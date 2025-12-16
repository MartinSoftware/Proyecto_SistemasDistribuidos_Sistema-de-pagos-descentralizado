# 🔗 Proyecto del curso de Sistemas Distribuidos - UTP Lima Norte
Sistema de Pagos Descentralizado - Blockchain

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

Un sistema de pagos completamente **descentralizado** implementado con blockchain privado. Red P2P con múltiples nodos que utilizan **criptografía RSA** para transacciones seguras, **Proof of Work** para consenso distribuido y una interfaz web en tiempo real.

> **Proyecto Universitario**: Demuestra los principios fundamentales de sistemas distribuidos, blockchain y criptografía de clave pública.

---

## ✨ Características Principales

### 🔐 Seguridad Criptográfica
- **Criptografía RSA 2048-bit**: Firma digital de todas las transacciones
- **Hash SHA-256**: Garantía de integridad de bloques
- **Validación de firmas**: Verificación criptográfica en cada transacción

### 🌐 Arquitectura Distribuida
- **Red P2P**: Múltiples nodos independientes (Alice, Bob, Charlie)
- **Sincronización automática**: Réplica de blockchain entre participantes
- **Sin punto central de fallo**: Descentralización completa
- **Consenso mediante PoW**: Proof of Work con dificultad ajustable

### 💼 Gestión de Wallets
- **Billeteras digitales**: Una por participante con par de claves RSA
- **Direcciones únicas**: Derivadas del hash de clave pública (40 caracteres)
- **Balance automático**: Cálculo de saldos desde el historial de transacciones

### 📊 Transparencia
- **Registro inmutable**: Todas las transacciones quedan registradas
- **Dashboard web**: Interfaz en tiempo real con estado de la red
- **Historial completo**: Trazabilidad de todas las operaciones

---

## 🚀 Inicio Rápido

### Requisitos Previos

```bash
Python 3.8 o superior
pip (gestor de paquetes)
```

### Instalación

1. **Clona el repositorio**
```bash
git clone https://github.com/MartinSoftware/Proyecto_SistemasDistribuidos_Sistema-de-pagos-descentralizado.git
cd Proyecto_SistemasDistribuidos_Sistema-de-pagos-descentralizado
```

2. **Instala las dependencias**

Las dependencias principales son:
- `Flask` - Framework web
- `Flask-CORS` - Soporte de CORS
- `cryptography` - Librería de criptografía
- `requests` - Cliente HTTP

### Ejecución

#### Opción 1: Demostración Automática (Windows)
```bash
python demo_automatico.py
```
O simplemente ejecuta:
```bash
run_demo.bat
```

#### Opción 2: Iniciar Nodos Manualmente
```bash
# Terminal 1 - Nodo Alice (puerto 5000)
python blockchain.py --port 5000 --name alice

# Terminal 2 - Nodo Bob (puerto 5001)
python blockchain.py --port 5001 --name bob

# Terminal 3 - Nodo Charlie (puerto 5002)
python blockchain.py --port 5002 --name charlie
```

3. **Accede al Dashboard**
```
http://localhost:5000/dashboard
```

---

## 📁 Estructura del Proyecto

```
.
├── blockchain.py              # Core del sistema (Wallet, Transaction, Blockchain, API)
├── demo_automatico.py         # Script de demostración automática
├── dashboard.html             # Interfaz web en tiempo real
├── run_demo.bat              # Lanzador de demostración (Windows)
├── detener_nodos.bat         # Script para detener nodos (Windows)
├── verificar_requisitos.bat  # Verifica dependencias (Windows)
├── logs/                     # Directorio de registros
├── INFORME_PROYECTO.md       # Informe detallado del proyecto
└── README.md                 # Este archivo

```

---

## 🏗️ Arquitectura Técnica

### Componentes Principales

#### 1. **Wallet (Billetera Digital)**
```python
wallet = Wallet("Alice")
address = wallet.get_address()        # Dirección única
public_key = wallet.get_public_key_pem()  # Clave pública
signature = wallet.sign_transaction(data)  # Firma transacción
```

#### 2. **Transaction (Transacción)**
- Estructura inmutable con: remitente, destinatario, cantidad, timestamp
- Firma digital RSA para autenticidad
- Validación de firma mediante clave pública del remitente

#### 3. **Block (Bloque)**
- Índice, timestamp, lista de transacciones, hash anterior, nonce
- Método `calculate_hash()`: Genera hash SHA-256
- Método `mine_block()`: Implementa Proof of Work

#### 4. **Blockchain (Cadena de Bloques)**
- Bloque génesis inicial
- Validación de transacciones y balances
- Minería de bloques con dificultad ajustable
- Cálculo de balances desde el historial

#### 5. **Red P2P**
- API REST con Flask en cada nodo
- Endpoints para transacciones, minería y sincronización
- Comunicación HTTP entre nodos
- Replicación automática de blockchain

---

## 🔌 API REST Endpoints

### Nodo Individual

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/chain` | Obtiene la blockchain completa |
| GET | `/balance/<address>` | Consulta balance de una dirección |
| POST | `/transaction` | Envía una transacción |
| POST | `/mine` | Mina un bloque |
| GET | `/pending-transactions` | Lista transacciones pendientes |
| GET | `/sync` | Solicita sincronización |
| GET | `/dashboard` | Interfaz web |

### Ejemplo de Solicitud (cURL)

```bash
# Crear transacción
curl -X POST http://localhost:5000/transaction \
  -H "Content-Type: application/json" \
  -d '{
    "sender_address": "Alice",
    "recipient_address": "Bob",
    "amount": 50
  }'

# Minar bloque
curl -X POST http://localhost:5000/mine \
  -H "Content-Type: application/json" \
  -d '{"miner_address": "Alice"}'

# Consultar balance
curl http://localhost:5000/balance/alice_address
```

---

## 💡 Casos de Uso Demostrados

✅ **Transferencia de fondos** entre usuarios sin intermediarios  
✅ **Validación criptográfica** de transacciones  
✅ **Minería descentralizada** con Proof of Work  
✅ **Sincronización automática** de blockchain entre nodos  
✅ **Detección de fraude** - Transacciones inválidas rechazadas  
✅ **Recompensas de minería** automáticas  
✅ **Consultas de saldo** en tiempo real  
✅ **Historial de transacciones** completo e inmutable  

---

## 🎓 Conceptos Educativos

Este proyecto implementa y demuestra:

| Concepto | Implementación |
|----------|-----------------|
| **Criptografía Asimétrica** | RSA 2048-bit para firma de transacciones |
| **Hash Criptográfico** | SHA-256 para identificación de bloques |
| **Proof of Work (PoW)** | Minería con búsqueda de nonce |
| **Consenso Distribuido** | Validación y sincronización entre nodos |
| **Arquitectura P2P** | Red descentralizada sin servidor central |
| **API REST** | Comunicación HTTP entre participantes |
| **Sistemas Distribuidos** | Múltiples nodos trabajando en paralelo |
| **Inmutabilidad** | Cadena de bloques de solo lectura |
| **Trazabilidad** | Auditoría completa de todas las operaciones |

---

## 📊 Flujo de Funcionamiento

```
┌─────────────────────────────────────────────────────────┐
│              SISTEMA DE PAGOS DESCENTRALIZADO            │
└─────────────────────────────────────────────────────────┘

1️⃣  INICIACIÓN
   └─ Cada nodo genera su wallet con par de claves RSA

2️⃣  TRANSACCIÓN
   └─ Usuario crea transacción
   └─ Se firma digitalmente con clave privada
   └─ Se propaga a través de la red

3️⃣  VALIDACIÓN
   └─ Cada nodo verifica la firma digital
   └─ Se valida que el remitente tenga saldo suficiente
   └─ Transacción se agrega a pendientes

4️⃣  MINERÍA
   └─ Minero recolecta transacciones pendientes
   └─ Ejecuta Proof of Work (busca nonce válido)
   └─ Genera nuevo bloque con transacciones validadas

5️⃣  CONSENSO
   └─ Nuevo bloque se propaga a la red
   └─ Cada nodo valida el bloque
   └─ Blockchain se actualiza en todos los participantes

6️⃣  FINALIDAD
   └─ Transacción es inmutable y registrada permanentemente
   └─ Saldos se actualizan en toda la red
   └─ Minero recibe recompensa de 10 monedas
```

---

## 🎯 Casos de Prueba

Ejecuta la demostración automática para ver:

```python
# Alice transfiere a Bob
# Bob transfiere a Charlie
# Charlie transfiere a Alice
# Minería en cada nodo
# Sincronización de blockchain
# Validación de transacciones inválidas
# Cálculo de balances
```

---

## 🔧 Configuración Avanzada

### Ajustar Dificultad de Minería

Edita `blockchain.py`:
```python
self.difficulty = 2  # Cambiar a 3, 4, 5... (más difícil)
```

### Cambiar Recompensa de Minería

```python
self.mining_reward = 10  # Cambiar a otro valor
```

### Agregar Más Nodos

```python
python blockchain.py --port 5003 --name david
```

---

## 📈 Estadísticas del Proyecto

- **Líneas de código**: ~650 (blockchain.py)
- **Clases principales**: 5 (Wallet, Transaction, Block, Blockchain, + API)
- **Endpoints API**: 7+
- **Nodos de demostración**: 3 (Alice, Bob, Charlie)
- **Algoritmo de hash**: SHA-256
- **Criptografía**: RSA 2048-bit

---

## 🐛 Troubleshooting

### Puerto ya en uso
```bash
# Cambia el puerto
python blockchain.py --port 5003
```

### Dependencias no instaladas
```bash
pip install -r requirements.txt --upgrade
```

### Problemas de CORS
Las conexiones están configuradas con CORS habilitado. Verifica `flask_cors.CORS(app)`.

### Nodos desincronizados
- Ejecuta sincronización manual: `/sync`
- O reinicia todos los nodos

---

## 📚 Documentación Adicional

- [`INFORME_PROYECTO.md`](INFORME_PROYECTO.md) - Informe detallado del sistema
- Comentarios en `blockchain.py` - Explicaciones de código
- `demo_automatico.py` - Ejemplos de uso

---

## 🔐 Consideraciones de Seguridad

⚠️ **Este es un proyecto educativo.** No usar en producción. Limitaciones:

- Base de datos en memoria (no persiste)
- Red local/privada (sin encriptación de comunicaciones)
- Dificultad de PoW muy baja (para demostración rápida)
- Sin mecanismos de rate limiting o DDoS protection
- Wallets sin contraseña (solo claves RSA)

Para producción, considera:
- Almacenamiento persistente
- TLS/HTTPS para comunicaciones
- Mayor dificultad de PoW
- Validación y sanitización completa
- Mecanismos de autenticación robustos

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---


## 👤 Autor

**MartinSoftware**

- GitHub: [@MartinSoftware](https://github.com/MartinSoftware)
- Proyecto: [Sistema de Pagos Descentralizado](https://github.com/MartinSoftware/Proyecto_SistemasDistribuidos_Sistema-de-pagos-descentralizado)

---

## 📊 Estado del Proyecto

| Aspecto | Estado |
|--------|--------|
| Core Blockchain | ✅ Completo |
| API REST | ✅ Funcional |
| Dashboard Web | ✅ Funcional |
| Criptografía | ✅ Implementada |
| Red P2P | ✅ Operativa |
| Demostración | ✅ Automatizada |
| Documentación | ✅ Completa |

---

**Última actualización**: 2 de diciembre de 2025  
**Versión**: 1.0  
**Estatus**: 🟢 Activo y Funcional
