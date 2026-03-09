# 🎓 SGE - Sistema de Gestión Estudiantil

Proyecto de **Ecosistemas NoSQL** enfocado en la aceleración de consultas utilizando **Redis**, **Flask** y **Docker**.

## 📌 Descripción

El **SGE (Sistema de Gestión Estudiantil)** es una aplicación diseñada para gestionar registros académicos utilizando una base de datos **NoSQL basada en Redis**.

El sistema fue desarrollado para el **Escenario B: Aceleración de Consultas**, donde el objetivo principal es obtener tiempos de respuesta extremadamente rápidos mediante almacenamiento en memoria.

## 🛠 Tecnologías utilizadas

- Redis
- Flask
- Docker
- Python

## 🧠 Justificación Técnica

### Modelo de Datos: Clave-Valor (Hashes)

Para el SGE se eligió el modelo **clave-valor** utilizando **Hashes de Redis**.

Cada estudiante se almacena como un objeto dentro de una clave:

estudiante:ID

### Teorema de CAP

Redis se ubica dentro del modelo **CP (Consistencia y Tolerancia al Particionamiento)**.

## 📂 Operaciones CRUD en consola REDIS

### CREAR

HSET estudiante:101 nombre "Jairo Salgado" curso "Sistemas V" nota 5.0

### LEER

HGETALL estudiante:101

### ACTUALIZAR

HSET estudiante:101 nota 4.2

### ELIMINAR

DEL estudiante:101

## 👥 Integrantes

- Jairo Esteban Salgado Tinoco
- Juan Camilo Ballares Diaz
- Juan David Casanova Cortes