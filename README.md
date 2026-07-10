# Prueba Técnica Backend Developer

API REST desarrollada en Python con FastAPI para la importación y gestión de datos de archivo excel.

## Tecnologías Utilizadas

- **Backend**: FastAPI 0.139.0
- **Base de Datos**: PostgreSQL
- **ORM**: SQLAlchemy 2.0.51
- **Migraciones**: Alembic 1.18.5
- **Validación**: Pydantic 2.13.4
- **Procesamiento Excel**: Pandas, OpenPyXL

## Estructura del Proyecto

```
prueba_tecnica_backend_developer_python/
├── alembic/                  # Migraciones de base de datos
├── src/
│   ├── api/
│   │   └── routes/           # Endpoints de la API
│   ├── core/                 # Configuración del proyecto
│   ├── crud/                 # Operaciones CRUD
│   ├── databases/            # Conexión y sesiones de BD
│   ├── models/               # Modelos SQLAlchemy
│   ├── schemas/              # Esquemas Pydantic
│   └── services/             # Logica de negocio y validaciones
├── .dockerignore             # Archivos a ignorar en Docker
├── .env                      # Variables de entorno
├── alembic.ini               # Configuración de Alembic
├── docker-compose.yml        # Orquestación con Docker
├── Dockerfile                # Definición de la imagen Docker
└── requirements.txt          # Dependencias del proyecto
```

## Instalación y Configuración

### Opción 1: Instalación Manual

#### 1. Clonar el repositorio

```bash
cd prueba_tecnica_backend_developer_python
```

#### 2. Crear entorno virtual

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 4. Configurar variables de entorno

Editar el archivo `.env` con los datos de la base de datos PostgreSQL:

```env
DATABASE_URL=postgresql://usuario:contraseña@127.0.0.1/nombre_bd
```

#### 5. Ejecutar migraciones

```bash
alembic upgrade head
```

#### 6. Iniciar el servidor

```bash
uvicorn src.main:app --reload
```

El servidor estará disponible en: `http://localhost:8000`

---

### Opción 2: Docker

#### 1. Clonar el repositorio

```bash
cd prueba_tecnica_backend_developer_python
```

#### 2. Iniciar los servicios con Docker Compose

```bash
docker-compose up --build -d
```

Esto creará y ejecutará:
- **PostgreSQL 16**: Base de datos en el puerto 5432
- **FastAPI App**: Aplicación en el puerto 8000

Las migraciones se aplicarán automáticamente al iniciar.

#### 3. Verificar que los contenedores estén corriendo

```bash
docker-compose ps
```

#### 4. Detener los servicios

```bash
docker-compose down
```

#### 5. Ver logs de los contenedores

```bash
docker-compose logs -f
```

## Documentación de la API

Una vez iniciado el servidor, se puede acceder a la documentación automática:

- **Swagger UI**: `http://localhost:8000/docs`
- **Redoc**: `http://localhost:8000/redoc`

## Endpoints Disponibles

### CBAM

#### Importar archivo Excel

- **POST** `/cbam/upload`
- **Descripción**: Carga un archivo Excel con datos CBAM y valida su contenido
- **Body**: `multipart/form-data` con el campo `file`
- **Formato de archivo**: .xlsx
- **Encabezados requeridos**:
  - EORI Number
  - Declarant Legal Name
  - Declarant Address
  - Contact Person
  - Competent Authority
  - CBAM Account Number
  - Data Owner
  - TARIC Code
  - CN Code
  - Goods Description
  - Sector Category
  - Product Type
  - Import Volume
  - Date of importation
  - Country of Origin
  - Customs Declaration Ref
  - Supplier Name
  - Notes / Comments

## Modelo de Datos

### CbamImport

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer | ID primario autoincremental |
| eori_number | String(17) | Número EORI (obligatorio) |
| declarant_legal_name | String(255) | Nombre legal del declarante (obligatorio) |
| declarant_address | Text | Dirección del declarante (obligatorio) |
| contact_person | String(255) | Persona de contacto (obligatorio) |
| competent_authority | String(100) | Autoridad competente (obligatorio) |
| cbam_account_number | String(100) | Número de cuenta CBAM (obligatorio) |
| data_owner | String(255) | Propietario de los datos (obligatorio) |
| taric_code | String(10) | Código TARIC |
| cn_code | String(8) | Código CN (obligatorio) |
| goods_description | Text | Descripción de mercancías (obligatorio) |
| sector_category | String(100) | Categoría de sector (obligatorio) |
| product_type | String(20) | Tipo de producto (obligatorio) |
| import_volume | Numeric(12,2) | Volumen de importación (obligatorio) |
| date_of_importation | Date | Fecha de importación (obligatorio) |
| country_of_origin | String(100) | País de origen (obligatorio) |
| customs_declaration_ref | String(100) | Referencia de declaración aduanera (obligatorio) |
| supplier_name | String(255) | Nombre del proveedor (obligatorio) |
| notes_comments | Text | Notas y comentarios |

## Migraciones con Alembic

### Crear una nueva migración

```bash
alembic revision --autogenerate -m "descripcion_de_la_migracion"
```

### Aplicar migraciones

```bash
alembic upgrade head
```

### Revertir última migración

```bash
alembic downgrade -1
```

## Pruebas Automatizadas

El proyecto incluye pruebas automatizadas con pytest. Para ejecutarlas:

1. Tener las dependencias de testing instaladas (se incluyen en `requirements.txt`):

```bash
pip install -r requirements.txt
```

2. Ejecuta todas las pruebas:

```bash
pytest
```

O ejecuta las pruebas con más detalle:

```bash
pytest -v
```

Las pruebas se encuentran en el directorio `test/` y usan una base de datos SQLite en memoria para aislar el entorno de testing.

## Autor

Ana Huertas
