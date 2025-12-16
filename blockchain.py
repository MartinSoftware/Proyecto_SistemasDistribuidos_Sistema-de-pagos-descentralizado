from flask import Flask, jsonify, request
from flask_cors import CORS
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import hashlib
import json
import time
from datetime import datetime
import requests

# ==================== WALLET ====================
class Wallet:
    """Billetera digital con par de claves RSA"""
    def __init__(self, owner_name):
        self.owner_name = owner_name
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
        
    def get_address(self):
        """Obtiene la dirección de la wallet (hash de la clave pública)"""
        public_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return hashlib.sha256(public_bytes).hexdigest()[:40]
    
    def sign_transaction(self, transaction_data):
        """Firma una transacción con la clave privada"""
        message = json.dumps(transaction_data, sort_keys=True).encode()
        signature = self.private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature.hex()
    
    def get_public_key_pem(self):
        """Retorna la clave pública en formato PEM"""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

# ==================== TRANSACTION ====================
class Transaction:
    """Transacción entre dos wallets"""
    def __init__(self, sender_address, recipient_address, amount, sender_public_key):
        self.sender_address = sender_address
        self.recipient_address = recipient_address
        self.amount = amount
        self.timestamp = time.time()
        self.sender_public_key = sender_public_key
        self.signature = None
        
    def to_dict(self):
        return {
            'sender_address': self.sender_address,
            'recipient_address': self.recipient_address,
            'amount': self.amount,
            'timestamp': self.timestamp,
            'sender_public_key': self.sender_public_key
        }
    
    def sign_transaction(self, signature):
        self.signature = signature
        
    def is_valid(self):
        """Verifica la firma digital de la transacción"""
        if self.sender_address == "MINING_REWARD":
            return True
            
        if not self.signature:
            return False
            
        try:
            public_key = serialization.load_pem_public_key(
                self.sender_public_key.encode(),
                backend=default_backend()
            )
            
            message = json.dumps(self.to_dict(), sort_keys=True).encode()
            public_key.verify(
                bytes.fromhex(self.signature),
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception as e:
            print(f"Error verificando firma: {e}")
            return False

# ==================== BLOCK ====================
class Block:
    """Bloque de la blockchain"""
    def __init__(self, index, transactions, previous_hash, nonce=0):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
        
    def calculate_hash(self):
        """Calcula el hash del bloque"""
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty):
        """Minado del bloque (Proof of Work)"""
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"✅ Bloque minado: {self.hash}")

# ==================== BLOCKCHAIN ====================
class Blockchain:
    """Cadena de bloques principal"""
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2
        self.pending_transactions = []
        self.mining_reward = 10
        
    def create_genesis_block(self):
        """Crea el bloque génesis (primer bloque)"""
        return Block(0, [], "0")
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def add_transaction(self, transaction):
        """Agrega una transacción pendiente"""
        if not transaction.is_valid():
            raise Exception("Transacción inválida")
        
        # Solo verificar balance si NO es una recompensa de minado
        if transaction.sender_address != "MINING_REWARD":
            sender_balance = self.get_balance(transaction.sender_address)
            if sender_balance < transaction.amount:
                raise Exception("Balance insuficiente")
            
        self.pending_transactions.append(transaction)
        return True
    
    def mine_pending_transactions(self, mining_reward_address):
        """Mina las transacciones pendientes"""
        # Crear transacción de recompensa
        reward_tx = Transaction(
            "MINING_REWARD",
            mining_reward_address,
            self.mining_reward,
            "SYSTEM"
        )
        
        # Agregar la recompensa a las transacciones pendientes
        self.pending_transactions.append(reward_tx)
        
        # Crear el bloque con TODAS las transacciones (incluyendo la recompensa)
        block = Block(
            len(self.chain),
            self.pending_transactions.copy(),  # Usar copia para no perder referencia
            self.get_latest_block().hash
        )
        
        # Minar el bloque
        print(f"⛏️  Minando bloque con {len(self.pending_transactions)} transacciones...")
        block.mine_block(self.difficulty)
        
        # Agregar el bloque a la cadena
        self.chain.append(block)
        
        # Limpiar transacciones pendientes
        self.pending_transactions = []
        
        print(f"✅ Bloque #{block.index} agregado a la cadena")
        return block
        
    def get_balance(self, address):
        """Obtiene el balance de una dirección"""
        balance = 0
        
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender_address == address:
                    balance -= tx.amount
                if tx.recipient_address == address:
                    balance += tx.amount
                    
        return balance
    
    def is_chain_valid(self):
        """Verifica la integridad de la blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            
            if current_block.previous_hash != previous_block.hash:
                return False
            
            for tx in current_block.transactions:
                if not tx.is_valid():
                    return False
                    
        return True

# ==================== NODO (API REST) ====================
app = Flask(__name__)
CORS(app)
app.config['PORT'] = 5000

blockchain = Blockchain()
node_wallet = None
peer_nodes = set()

@app.route('/wallet/create', methods=['POST'])
def create_wallet():
    """Crea una nueva wallet"""
    global node_wallet
    data = request.get_json()
    owner_name = data.get('owner_name', 'Anonymous')
    
    node_wallet = Wallet(owner_name)
    
    return jsonify({
        'message': 'Wallet creada exitosamente',
        'owner': owner_name,
        'address': node_wallet.get_address(),
        'balance': blockchain.get_balance(node_wallet.get_address())
    }), 201

@app.route('/wallet/info', methods=['GET'])
def wallet_info():
    """Obtiene información de la wallet del nodo"""
    if not node_wallet:
        return jsonify({'error': 'No hay wallet en este nodo'}), 400
    
    return jsonify({
        'owner': node_wallet.owner_name,
        'address': node_wallet.get_address(),
        'balance': blockchain.get_balance(node_wallet.get_address())
    })

@app.route('/transaction/create', methods=['POST'])
def create_transaction():
    """Crea y firma una nueva transacción"""
    if not node_wallet:
        return jsonify({'error': 'Primero crea una wallet'}), 400
    
    data = request.get_json()
    recipient = data.get('recipient_address')
    amount = data.get('amount')
    
    if not recipient or not amount:
        return jsonify({'error': 'Faltan datos'}), 400
    
    try:
        tx = Transaction(
            node_wallet.get_address(),
            recipient,
            float(amount),
            node_wallet.get_public_key_pem()
        )
        
        signature = node_wallet.sign_transaction(tx.to_dict())
        tx.sign_transaction(signature)
        
        blockchain.add_transaction(tx)
        print(f"✅ TX creada localmente: {amount} tokens")
        
        # Propagar a peers
        broadcast_transaction(tx)
        
        return jsonify({
            'message': 'Transacción creada y propagada',
            'transaction': {
                'sender': tx.sender_address,
                'recipient': tx.recipient_address,
                'amount': tx.amount,
                'timestamp': datetime.fromtimestamp(tx.timestamp).strftime('%Y-%m-%d %H:%M:%S')
            },
            'pending_count': len(blockchain.pending_transactions)
        }), 201
    except Exception as e:
        print(f"❌ Error creando transacción: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/mine', methods=['POST'])
def mine_block():
    """Mina un nuevo bloque con las transacciones pendientes"""
    if not node_wallet:
        return jsonify({'error': 'Primero crea una wallet para recibir recompensas'}), 400
    
    # Mostrar transacciones pendientes antes de minar
    pending_count = len(blockchain.pending_transactions)
    print(f"\n⛏️  Iniciando minado...")
    print(f"📋 Transacciones pendientes: {pending_count}")
    
    for i, tx in enumerate(blockchain.pending_transactions):
        print(f"   {i+1}. {tx.sender_address[:10]}... → {tx.recipient_address[:10]}... ({tx.amount} tokens)")
    
    # Obtener balance ANTES de minar
    balance_before = blockchain.get_balance(node_wallet.get_address())
    
    # Minar el bloque (esto incluye la recompensa automáticamente)
    block = blockchain.mine_pending_transactions(node_wallet.get_address())
    
    # Obtener balance DESPUÉS de minar
    balance_after = blockchain.get_balance(node_wallet.get_address())
    
    print(f"✅ Bloque minado con {len(block.transactions)} transacciones")
    print(f"💰 Balance: {balance_before} → {balance_after} tokens")
    
    # Propagar el nuevo bloque a los peers
    broadcast_new_block()
    
    return jsonify({
        'message': 'Bloque minado exitosamente',
        'reward': blockchain.mining_reward,
        'balance_before': balance_before,
        'new_balance': balance_after,
        'blocks_count': len(blockchain.chain),
        'block_index': block.index,
        'block_hash': block.hash,
        'transactions_in_block': len(block.transactions)
    })

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    """Obtiene la blockchain completa"""
    chain_data = []
    for block in blockchain.chain:
        chain_data.append({
            'index': block.index,
            'timestamp': datetime.fromtimestamp(block.timestamp).strftime('%Y-%m-%d %H:%M:%S'),
            'transactions': len(block.transactions),
            'hash': block.hash,
            'previous_hash': block.previous_hash,
            'nonce': block.nonce
        })
    
    return jsonify({
        'length': len(blockchain.chain),
        'chain': chain_data,
        'valid': blockchain.is_chain_valid()
    })

@app.route('/blockchain/full', methods=['GET'])
def get_full_blockchain():
    """Obtiene la blockchain con todas las transacciones"""
    chain_data = []
    for block in blockchain.chain:
        transactions = []
        for tx in block.transactions:
            transactions.append({
                'sender': tx.sender_address,
                'recipient': tx.recipient_address,
                'amount': tx.amount,
                'timestamp': datetime.fromtimestamp(tx.timestamp).strftime('%Y-%m-%d %H:%M:%S')
            })
        
        chain_data.append({
            'index': block.index,
            'timestamp': datetime.fromtimestamp(block.timestamp).strftime('%Y-%m-%d %H:%M:%S'),
            'transactions': transactions,
            'hash': block.hash,
            'previous_hash': block.previous_hash
        })
    
    return jsonify({'chain': chain_data})

@app.route('/blockchain/export', methods=['GET'])
def export_blockchain():
    """Exporta la blockchain completa para sincronización"""
    chain_data = []
    
    for block in blockchain.chain:
        transactions = []
        for tx in block.transactions:
            transactions.append({
                'sender_address': tx.sender_address,
                'recipient_address': tx.recipient_address,
                'amount': tx.amount,
                'timestamp': tx.timestamp,
                'sender_public_key': tx.sender_public_key,
                'signature': tx.signature
            })
        
        chain_data.append({
            'index': block.index,
            'timestamp': block.timestamp,
            'transactions': transactions,
            'hash': block.hash,
            'previous_hash': block.previous_hash,
            'nonce': block.nonce
        })
    
    return jsonify({
        'length': len(blockchain.chain),
        'chain': chain_data,
        'valid': blockchain.is_chain_valid()
    })

@app.route('/blockchain/sync', methods=['POST'])
def sync_blockchain():
    """Sincroniza la blockchain con otro nodo"""
    data = request.get_json()
    peer_url = data.get('peer_url')
    
    if not peer_url:
        return jsonify({'error': 'No se proporcionó peer_url'}), 400
    
    try:
        print(f"\n🔄 Intentando sincronizar con {peer_url}...")
        
        # Obtener la blockchain del peer
        response = requests.get(f"{peer_url}/blockchain/export", timeout=10)
        if response.status_code != 200:
            print(f"❌ No se pudo obtener blockchain del peer: {response.status_code}")
            return jsonify({'error': 'No se pudo obtener blockchain del peer'}), 400
        
        peer_data = response.json()
        peer_chain_data = peer_data.get('chain', [])
        
        local_length = len(blockchain.chain)
        peer_length = len(peer_chain_data)
        
        print(f"📊 Longitudes - Local: {local_length}, Peer: {peer_length}")
        
        # Si la cadena del peer es más larga, reemplazar
        if peer_length > local_length:
            print(f"⬇️  La cadena del peer es más larga. Sincronizando...")
            
            # Crear una nueva cadena temporal
            temp_chain = []
            
            for block_data in peer_chain_data:
                transactions = []
                
                # Reconstruir transacciones
                for tx_data in block_data.get('transactions', []):
                    tx = Transaction(
                        tx_data['sender_address'],
                        tx_data['recipient_address'],
                        tx_data['amount'],
                        tx_data['sender_public_key']
                    )
                    tx.timestamp = tx_data['timestamp']
                    if tx_data.get('signature'):
                        tx.sign_transaction(tx_data['signature'])
                    transactions.append(tx)
                
                # Crear bloque
                block = Block(
                    block_data['index'],
                    transactions,
                    block_data['previous_hash'],
                    block_data.get('nonce', 0)
                )
                
                # CRÍTICO: Asignar timestamp ANTES de asignar el hash
                block.timestamp = block_data['timestamp']
                
                # Ahora asignar el hash (que ya está calculado con este timestamp)
                block.hash = block_data['hash']
                
                temp_chain.append(block)
            
            # Validación manual
            is_valid = True
            
            for i in range(1, len(temp_chain)):
                current = temp_chain[i]
                previous = temp_chain[i-1]
                
                if current.previous_hash != previous.hash:
                    print(f"❌ Bloque {i}: previous_hash no coincide")
                    is_valid = False
                    break
                
                if not current.hash.startswith('0' * blockchain.difficulty):
                    print(f"❌ Bloque {i}: No cumple dificultad de PoW")
                    is_valid = False
                    break
            
            if is_valid:
                print(f"✅ Cadena del peer es válida. Reemplazando local...")
                blockchain.chain = temp_chain
                blockchain.pending_transactions = []
                print(f"✅ Sincronización completada: {local_length} -> {peer_length} bloques")
                return jsonify({
                    'message': 'Blockchain sincronizada exitosamente',
                    'old_length': local_length,
                    'new_length': len(blockchain.chain)
                }), 200
            else:
                print(f"❌ La cadena del peer NO pasó la validación")
                return jsonify({'error': 'Blockchain del peer es inválida'}), 400
        else:
            print(f"ℹ️  La blockchain local ya está actualizada o es más larga")
            return jsonify({
                'message': 'La blockchain local ya está actualizada',
                'length': len(blockchain.chain)
            }), 200
            
    except Exception as e:
        print(f"❌ Error en sincronización: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Error en sincronización: {str(e)}'}), 500

@app.route('/balance/<address>', methods=['GET'])
def get_balance(address):
    """Obtiene el balance de una dirección"""
    balance = blockchain.get_balance(address)
    return jsonify({'address': address, 'balance': balance})

@app.route('/peers/register', methods=['POST'])
def register_peer():
    """Registra un nodo peer"""
    data = request.get_json()
    peer_url = data.get('peer_url')
    
    if peer_url:
        peer_nodes.add(peer_url)
        return jsonify({'message': 'Peer registrado', 'peers': list(peer_nodes)}), 201
    return jsonify({'error': 'URL inválida'}), 400

@app.route('/peers', methods=['GET'])
def get_peers():
    """Lista todos los peers"""
    return jsonify({'peers': list(peer_nodes)})

def broadcast_transaction(transaction):
    """Propaga una transacción a todos los nodos peer"""
    tx_dict = transaction.to_dict()
    tx_dict['signature'] = transaction.signature
    
    for peer in peer_nodes:
        try:
            print(f"📡 Propagando TX a {peer}...")
            response = requests.post(
                f"{peer}/transaction/receive", 
                json=tx_dict,
                timeout=2
            )
            if response.status_code == 200:
                print(f"✅ TX recibida por {peer}")
            else:
                print(f"⚠️  {peer} respondió: {response.status_code}")
        except Exception as e:
            print(f"❌ Error propagando a {peer}: {str(e)}")

def broadcast_new_block():
    """Propaga un nuevo bloque a todos los peers"""
    for peer in peer_nodes:
        try:
            requests.post(
                f"{peer}/blockchain/sync",
                json={'peer_url': f"http://localhost:{app.config['PORT']}"},
                timeout=5
            )
        except:
            pass

@app.route('/transaction/receive', methods=['POST'])
def receive_transaction():
    """Recibe una transacción de otro nodo"""
    data = request.get_json()
    try:
        # Verificar si ya existe en pending_transactions
        tx_exists = False
        for pending_tx in blockchain.pending_transactions:
            if (pending_tx.sender_address == data['sender_address'] and
                pending_tx.recipient_address == data['recipient_address'] and
                pending_tx.amount == data['amount'] and
                pending_tx.timestamp == data['timestamp']):
                tx_exists = True
                break
        
        if tx_exists:
            print(f"⚠️  Transacción duplicada ignorada")
            return jsonify({'message': 'Transacción ya existe'}), 200
        
        tx = Transaction(
            data['sender_address'],
            data['recipient_address'],
            data['amount'],
            data['sender_public_key']
        )
        tx.timestamp = data['timestamp']
        
        if data.get('signature'):
            tx.sign_transaction(data['signature'])
        
        blockchain.add_transaction(tx)
        print(f"✅ Transacción recibida: {data['amount']} tokens")
        return jsonify({'message': 'Transacción recibida'}), 200
    except Exception as e:
        print(f"❌ Error recibiendo transacción: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'Sistema de Pagos Descentralizado - Blockchain',
        'endpoints': {
            'POST /wallet/create': 'Crear wallet',
            'GET /wallet/info': 'Info de wallet',
            'POST /transaction/create': 'Crear transacción',
            'POST /mine': 'Minar bloque',
            'GET /blockchain': 'Ver blockchain',
            'GET /blockchain/full': 'Ver blockchain completa',
            'GET /blockchain/export': 'Exportar blockchain',
            'POST /blockchain/sync': 'Sincronizar blockchain',
            'GET /balance/<address>': 'Consultar balance',
            'POST /peers/register': 'Registrar peer',
            'GET /peers': 'Listar peers'
        }
    })

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.config['PORT'] = port
    print(f"\n🚀 Nodo iniciado en puerto {port}")
    print(f"📡 Accede a: http://localhost:{port}/")
    app.run(host='0.0.0.0', port=port, debug=True)