# Sistema de Tracking y Reidentificación de Jugadores en Fútbol Amateur

**Alumno/a:** Juan Ignacio Soriano Muñoz  
**Titulación:** Ingeniería de la Salud  
**Tutore/s:** Rafael Marcos Luque Baena, Jose Manuel Jerez Aragonés  
**Título en inglés:** Player tracking and re-identification in amateur football using object detection  

## Introducción

El análisis de partidos de fútbol ha evolucionado significativamente con el uso de tecnologías avanzadas de visión artificial y seguimiento de jugadores. Sin embargo, en el ámbito del fútbol amateur, estas soluciones aún presentan desafíos debido a la falta de infraestructura y la variabilidad en las condiciones de grabación.

Este proyecto tiene como objetivo desarrollar una herramienta accesible y eficiente para el tracking automatizado de jugadores en partidos de fútbol amateur. Utiliza tecnologías de **Multi-Object Tracking (MOT)** y **Re-Identification (ReID)** para asignar identificadores consistentes a los jugadores, incluso cuando salen del campo de visión o se superponen con otros jugadores.

La solución propuesta se basa en modelos preentrenados, sin requerir hardware especializado, y está diseñada para optimizar su aplicabilidad en el ámbito del fútbol amateur, mejorando la experiencia de entrenadores y jugadores.

El proyecto estará basado en un estudio previo realizado por Jiacheng Sun. Estará referenciado en el apartado de [Referencias](#referencias).

## Objetivos

El objetivo principal de este TFG es desarrollar una aplicación capaz de realizar el seguimiento y la reidentificación de jugadores durante los partidos de fútbol amateur. Algunas de las funcionalidades clave del sistema incluyen:

- **Tracking de jugadores:** Utilizando modelos de visión artificial para detectar y seguir a los jugadores a lo largo del partido.
- **Reidentificación de jugadores:** Integración de un sistema que minimiza la pérdida de identidad, incluso cuando los jugadores desaparecen temporalmente del campo de visión.
- **Corrección manual:** Notificación al usuario cuando se detectan cambios inesperados en los identificadores de los jugadores, permitiendo correcciones manuales.
- **Reentrenamiento automatizado:** Generación de anotaciones para reentrenar el modelo, optimizando el sistema con el tiempo.

https://github.com/user-attachments/assets/5c362a27-de44-4d9b-9edf-1b46f06a27b4

## Entregables

- **Aplicación de seguimiento y reidentificación de jugadores.**  
- **Documentación técnica.**  
- **Estudio de viabilidad y validación del sistema.**  
- **Informe final y presentación.**  
- **Manual de usuario.**

## Metodología

Este proyecto sigue una metodología **iterativa y ágil** para abordar los desafíos específicos del tracking y la reidentificación de jugadores en fútbol amateur. Las fases de trabajo incluyen:

1. **Estudio inicial y definición de requisitos.**  
2. **Selección y preparación de datos.**  
3. **Implementación del modelo de tracking (YOLO).**  
4. **Desarrollo del módulo de reidentificación.**  
5. **Testeo y ajuste del sistema.**  
6. **Desarrollo de la interfaz de usuario.**  
7. **Validación y documentación.**

## Entorno Tecnológico

### Tecnologías empleadas

- **Lenguajes de programación:** Python, JavaScript
- **Frameworks y librerías:** Angular, YOLO, Hugging Face
- **Bases de datos:** SQL
- **Herramientas de desarrollo:** Git, Visual Studio Code, Jupyter Notebook, TexStudio, Overleaf

### Recursos de software

- **Plataformas:** GitHub, Hugging Face
- **Herramientas de anotación:** Roboflow Annotate, CVAT
- **IDE/Editor:** Visual Studio Code, TexStudio

## Fases de Trabajo

| Fase                                | Horas |
|-------------------------------------|-------|
| Estudio inicial y definición de requisitos | 20    |
| Selección y preparación de datos    | 50    |
| Implementación del modelo de tracking | 30    |
| Desarrollo del módulo de reidentificación | 50    |
| Testeo y ajuste del sistema         | 50    |
| Desarrollo de la interfaz de usuario | 43    |
| Validación y documentación          | 53    |
| **Total**                           | **296** |

## Dataset Etiquetado

Este dataset incluye anotaciones de bounding boxes, identificadores de jugadores y clases, siguiendo el formato de SoccerNet, pero adaptado a las necesidades concretas del proyecto para el contexto de fútbol amateur.

Dataset etiquetado desde el siguiente enlace:

[Dataset etiquetado para ReID de futbol amateur](https://drive.google.com/file/d/19JdrNt9_aiiNRV_AndWeEoMUuCuVx_HI/view?usp=sharing)


## Modelos Usados

Para la tarea de **reidentificación de jugadores**, se han utilizado varios modelos preentrenados con arquitecturas diversas, incluyendo redes convolucionales y transformadores. La siguiente tabla resume las características clave de cada modelo probado:

### Modelos entrenados con Dataset de SoccerNet (futbol profesional)

| name             | #params | Resolution | mAP  | rank-1 | chkpt                                                                                 | config                                                                                 |
|------------------|---------|------------|------|--------|----------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|
| ResNet50-fc512   | 24.6M   | 256x128    | 28.8 | 88.1   | [model](https://drive.google.com/file/d/1o45E8lxB9mxJ1lfSgMpi3mC0zUwVvzgz/view?usp=sharing) | [config](https://drive.google.com/file/d/1CqtCPpn9NSlZ5NMmGUqWfd-fcOOWVyOu/view?usp=sharing) |
| OSNet_x1_0       | 2.2M    | 256x128    | 30.3 | 90.4   | [model](https://drive.google.com/file/d/1To0Ww6_HxU2ITAlb4kQEgYExV-orwit8/view?usp=sharing) | [config](https://drive.google.com/file/d/1xO4Qe7f4FwpXnEe39cn24FdRDg6F-LLu/view?usp=sharing) |


### Modelos entrenados con Dataset de Sportsmot (futbol profesional)

| name             | #params | Resolution | mAP  | rank-1                                                                                  | config                                                                                 |
|------------------|---------|------------|------|--------|----------------------------------------------------------------------------------------|
| OSNet_x1_0       | 2.2M    | 256x128    | 28.6% | 91.3%   | [model](https://drive.google.com/file/d/1Wt_U-D2wfkMyKl1RIuIN2mAoM8M99jho/view?usp=sharing) |


### Modelos entrenados con Dataset propio (futbol amateur)
| name             | #params | Resolution | mAP  | rank-1                                                                                  | config                                                                                 |
|------------------|---------|------------|------|--------|----------------------------------------------------------------------------------------|
| OSNet_x1_0       | 2.2M    | 256x128    | 89.7% | 97.9%   | [model](https://drive.google.com/file/d/1i52wTC13yQ-HMI4R1tKdFqCP9TCotKAX/view?usp=sharing) |

Todo lo referente al entrenamiento del modelo con dataset de futbol amateur está en la carpeta [entrenamientoReID](https://github.com/JuanSoM/TFG---Player-tracking-and-re-identification-in-amateur-football-using-object-detection/tree/main/code/entrenamientoReID)

## Referencias

1. [Person Re-identification](https://paperswithcode.com/task/person-re-identification)
2. [SoccerNet](https://github.com/SoccerNet/sn-tracking)
3. [Sportsreid GitHub - shallowlearn](https://github.com/shallowlearn/sportsreid)
4. [Multi-object Tracking: A Review](https://sertiscorp.medium.com/multi-object-tracking-a-review-6aaeea495209)
5. ```bib
   @inproceedings{sun2024gta,
      title={GTA: Global Tracklet Association for Multi-Object Tracking in Sports},
      author={Sun, Jiacheng and Huang, Hsiang-Wei and Yang, Cheng-Yen and Hwang, Jenq-Neng},
      booktitle = {Proceedings of the Asian Conference on Computer Vision},
      pages = {421-434},
      year={2024},
      publisher = {Springer}
   }
6. ```bib
   @inproceedings{huang2024iterative,
      title={Iterative Scale-Up ExpansionIoU and Deep Features Association for Multi-Object Tracking in Sports},
      author={Huang, Hsiang-Wei and Yang, Cheng-Yen and Sun, Jiacheng and Kim, Pyong-Kun and Kim, Kwang-Ju and Lee, Kyoungoh and Huang, Chung-I and Hwang, Jenq-Neng},
      booktitle={Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision},
      pages={163--172},
      year={2024}
   }
## Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).
