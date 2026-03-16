**Watkit**
This API automates client management, providing automated follow-up triggers and structured data storage for client information.

**Tech stack**
*Framework:* FastAPI(High performance, easy to use).
*ORM:* SQLAlchemy(SQL database managment).
*Containerization:* Docker(Ensures consistent environment)
*Language:*Python 3.13+

**Project Architecture**
The application follows a layered structure to ensure scalability and clean code:
*Endpoinst(FastAPI):*Handles HTTP requests and routing.
*Schemas(Pydantic):*Validates client data(name, phone) before processing.
*Models(SQLAlchemy):* Defines the database table structure.
*Automation Logic:*Internal services that handle the automated follow-up sequences

**Docker Deployment**
To spin up the project quickly without manual environment configuration:
*Build the image:*
docker build -t watkit-api
*Run the container:*
docker run -d -p 8000:8000 watkit-API
----
**API Documentation**
Swagger UI: http://localhost:8000/docs (Test endpoints directly).

ReDoc: http://localhost:8000/redoc (Clean, read-only documentation).