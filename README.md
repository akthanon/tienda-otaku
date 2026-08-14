# 🛍️ Tienda Otaku - Proyecto de Práctica de Ciberseguridad

## 📖 Descripción del Proyecto

**Tienda Otaku** es una aplicación web de comercio electrónico diseñada específicamente como un campo de pruebas para prácticas de ciberseguridad. Este proyecto simula una tienda en línea funcional que vende productos relacionados con la cultura otaku (figuras de anime, mangas, accesorios, ediciones especiales), pero su verdadero propósito es servir como un entorno controlado para:

- **Identificar vulnerabilidades** comunes en aplicaciones web
- **Analizar riesgos de seguridad** en sistemas de comercio electrónico
- **Practicar técnicas de pentesting** en un ambiente seguro
- **Estudiar el impacto** de diferentes tipos de ataques
- **Desarrollar habilidades** en seguridad ofensiva y defensiva

La particularidad de este proyecto es que ha sido desarrollado con la asistencia de inteligencia artificial (IA), lo que lo convierte en un caso de estudio interesante sobre cómo las herramientas de IA pueden introducir vulnerabilidades en el código, incluso sin intención maliciosa.

## 🎯 Funcionalidades Principales

### Sistema de Autenticación
- **Registro de usuarios** con validación básica
- **Inicio de sesión** con manejo de sesiones
- **Cierre de sesión** seguro
- **Perfil de usuario** con estadísticas personales

### Catálogo de Productos
- **Visualización de productos** con imágenes, precios y descripciones
- **Filtrado por categorías**: Figuras, Mangas, Accesorios, Ediciones Especiales
- **Control de stock** con indicadores visuales de disponibilidad
- **Productos destacados** con sistema de etiquetas

### Carrito de Compras
- **Añadir productos** al carrito desde el catálogo
- **Modificar cantidades** de productos en el carrito
- **Eliminar productos** del carrito
- **Visualización del total** en tiempo real
- **Persistencia** del carrito durante la sesión

### Sistema de Pedidos
- **Proceso de checkout** con dirección de envío
- **Selección de métodos de pago** (Tarjeta, PayPal, OXXO, Efectivo)
- **Historial de pedidos** completo
- **Seguimiento de estados** (pendiente, pagado, enviado, entregado, cancelado)

### Interfaz de Usuario
- **Diseño moderno y responsive** adaptado a dispositivos móviles
- **Notificaciones toast** para feedback de acciones
- **Modales interactivos** para autenticación, carrito y checkout
- **Navegación intuitiva** con secciones claras

## 🏗️ Estructura del Proyecto

```
tienda-otaku/
├── backend/
│   ├── app.py              # API RESTful con Flask
│   ├── database.py         # Configuración de base de datos
│   ├── models.py           # Modelos de datos SQLAlchemy
│   └── requirements.txt    # Dependencias Python
├── frontend/
│   ├── images/             # Imágenes de productos
│   ├── index.html          # Página principal
│   ├── script.js           # Lógica del frontend
│   └── styles.css          # Estilos y diseño
├── docker-compose.yml      # Orquestación de contenedores
├── Dockerfile.backend      # Configuración del backend
└── Dockerfile.frontend     # Configuración del frontend
```

## 🔧 Tecnologías Utilizadas

### Backend
- **Flask 2.3.2** - Framework web ligero
- **SQLAlchemy 2.0.19** - ORM para base de datos
- **SQLite** - Base de datos por defecto
- **Flask-CORS** - Manejo de CORS

### Frontend
- **HTML5** - Estructura de la aplicación
- **CSS3** - Estilos modernos con diseño responsive
- **JavaScript (Vanilla)** - Lógica de cliente sin frameworks
- **Font Awesome 6** - Iconografía

### Infraestructura
- **Docker** - Contenerización de servicios
- **Docker Compose** - Orquestación multi-contenedor
- **Nginx** - Servidor web para archivos estáticos

## 🚀 Instalación y Ejecución

### Prerrequisitos
- Docker y Docker Compose instalados
- Git para clonar el repositorio

### Pasos para ejecutar el proyecto

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/tienda-otaku.git
cd tienda-otaku
```

2. **Configurar variables de entorno (opcional)**
```bash
# El proyecto usa valores por defecto, pero puedes modificarlos
# En backend/app.py puedes cambiar:
# - app.secret_key: Clave de sesión
# - CORS origins: Dominios permitidos
# - DATABASE_PATH: Ubicación de la base de datos
```

3. **Construir y levantar los contenedores**
```bash
docker-compose up -d --build
```

4. **Acceder a la aplicación**
- Frontend: http://localhost:48080
- Backend API: http://localhost:5000

5. **Detener la aplicación**
```bash
docker-compose down
```

### Configuración Adicional

#### Modificar Productos de Ejemplo
Los productos de ejemplo se crean automáticamente en `database.py`. Para modificarlos:

1. Edita el array `sample_products` en `database.py`
2. Reconstruye el contenedor:
```bash
docker-compose down
docker-compose up -d --build
```

#### Cambiar Métodos de Pago
Los métodos de pago se configuran en:
- **Frontend**: `index.html` en el select de métodos de pago
- **Backend**: `app.py` en el endpoint `/api/checkout`

## 🎯 Propósito de Seguridad

### Vulnerabilidades Potenciales para Estudio

Este proyecto ha sido desarrollado con IA, lo que introduce varias vulnerabilidades comunes que los estudiantes de ciberseguridad pueden identificar y explotar en un entorno controlado:

1. **Inyección SQL** en consultas de productos y autenticación
2. **XSS (Cross-Site Scripting)** en campos de entrada
3. **CSRF (Cross-Site Request Forgery)** en formularios
4. **Autenticación débil** sin medidas de seguridad avanzadas
5. **Exposición de datos sensibles** en respuestas API
6. **Validación de entrada insuficiente** en formularios
7. **Manejo inseguro de sesiones**
8. **Control de acceso inadecuado** en endpoints protegidos

### Áreas de Enfoque para Prácticas

| Área | Vulnerabilidades Comunes | Técnicas de Prueba |
|------|-------------------------|-------------------|
| Autenticación | SQL Injection, Brute Force | SQLMap, Hydra |
| Carrito de Compras | Manipulación de precios, IDOR | Burp Suite, Interceptación |
| Checkout | Inyección de datos, XSS | Payloads de XSS, Pruebas de entrada |
| API | Inyección, Autenticación | Postman, Curl, Fuzzing |
| Sesiones | Hijacking, Fixation | Análisis de cookies, Replay attacks |

## 📝 Personalización del Proyecto

### Modificar el Frontend
- **Estilos**: Edita `frontend/styles.css`
- **Contenido**: Modifica `frontend/index.html`
- **Lógica**: Actualiza `frontend/script.js`
- **Imágenes**: Añade imágenes en `frontend/images/`

### Modificar el Backend
- **Rutas API**: Añade o modifica rutas en `backend/app.py`
- **Modelos**: Actualiza `backend/models.py` para nuevas entidades
- **Base de datos**: Cambia el motor en `backend/database.py`

### Cambiar Puerto
En `docker-compose.yml`:
```yaml
ports:
  - "48080:80"    # Cambia 48080 por el puerto deseado
```

## 🤝 Contribución y Uso

Este proyecto está diseñado para fines educativos y de práctica en ciberseguridad. Se recomienda:

1. **Entorno de pruebas**: Usar en entornos aislados
2. **No utilizar en producción**: Este proyecto tiene vulnerabilidades intencionales
3. **Responsabilidad ética**: Practicar solo en sistemas propios o autorizados
4. **Documentar hallazgos**: Registrar vulnerabilidades encontradas y soluciones

## 📚 Recursos de Aprendizaje

Para aprovechar al máximo este proyecto como herramienta de aprendizaje:

1. **Fundamentos de Seguridad Web**
   - OWASP Top 10
   - Common Weakness Enumeration (CWE)
   - Secure Coding Practices

2. **Herramientas de Prueba**
   - Burp Suite
   - OWASP ZAP
   - SQLMap
   - Nmap
   - Wireshark

3. **Prácticas Recomendadas**
   - Realizar pruebas de penetración estructuradas
   - Documentar cada vulnerabilidad encontrada
   - Implementar soluciones para cada problema identificado
   - Comparar soluciones con las mejores prácticas de la industria

## ⚠️ Advertencia Legal

**Este proyecto contiene vulnerabilidades de seguridad intencionales y debe utilizarse SOLO en entornos educativos y controlados**. El uso de este software para atacar sistemas sin autorización explícita es ilegal y va contra los términos de uso de este proyecto.

---

## 📄 Licencia

Este proyecto está bajo licencia MIT - ver el archivo LICENSE para más detalles.

---

**¡Feliz aprendizaje y práctica de ciberseguridad!** 🔒
