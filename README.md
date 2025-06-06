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
| ResNet50-fc512   | 24.6M   | 256x128    | 28.8% | 88.1%   | [model](https://drive.google.com/file/d/1o45E8lxB9mxJ1lfSgMpi3mC0zUwVvzgz/view?usp=sharing) | [config](https://drive.google.com/file/d/1CqtCPpn9NSlZ5NMmGUqWfd-fcOOWVyOu/view?usp=sharing) |
| OSNet_x1_0       | 2.2M    | 256x128    | 30.3% | 90.4%   | [model](https://drive.google.com/file/d/1To0Ww6_HxU2ITAlb4kQEgYExV-orwit8/view?usp=sharing) | [config](https://drive.google.com/file/d/1xO4Qe7f4FwpXnEe39cn24FdRDg6F-LLu/view?usp=sharing) |


### Modelos entrenados con Dataset de Sportsmot (futbol profesional)

| name             | #params | Resolution | mAP  | rank-1                                                                                  | chkpt                                                                                 |
|------------------|---------|------------|------|--------|----------------------------------------------------------------------------------------|
| OSNet_x1_0       | 2.2M    | 256x128    | 28.6% | 91.3%   | [model](https://drive.google.com/file/d/1Wt_U-D2wfkMyKl1RIuIN2mAoM8M99jho/view?usp=sharing) |


### Modelos entrenados con Dataset propio (futbol amateur)
| name             | #params | Resolution | mAP  | rank-1                                                                                  | chkpt                                                                                 |
|------------------|---------|------------|------|--------|----------------------------------------------------------------------------------------|
| OSNet_x1_0       | 2.2M    | 256x128    | 89.7% | 97.9%   | [model](https://drive.google.com/file/d/1i52wTC13yQ-HMI4R1tKdFqCP9TCotKAX/view?usp=sharing) |

Todo lo referente al entrenamiento del modelo con dataset de futbol amateur está en la carpeta [entrenamientoReID](https://github.com/JuanSoM/TFG---Player-tracking-and-re-identification-in-amateur-football-using-object-detection/tree/main/code/entrenamientoReID)

## Flujo de trabajo resumido

### Primer capítulo (obtención del primer vídeo anotado)
Me centraré en la parte de ReID, ya que es la que más importancia tiene y es la que esta más desarrollada.

Se da por hecho que se han seguido los pasos de los readme de [DeepEIoU](https://github.com/hsiangwei0903/Deep-EIoU) y [gta-link](https://github.com/sjc042/gta-link), para tener paquetes instalados y setups ejecutados.

Para empezar tendremos que ejecutar el demo.py (Archivo de [DeepEIoU](https://github.com/hsiangwei0903/Deep-EIoU)) con un modelo soportado por torchreid. Por lo que habrá que cambiar el nombre del model. model_name. Con el objetivo de evitar este tipo de error:


KeyError: "Unknown model: model.resnet50.pth.tar-20. Must be one of ['resnet18', 'resnet34', 'resnet50', 'resnet101', 
'resnet152', 'resnext50_32x4d', 'resnext101_32x8d', 'resnet50_fc512', 'se_resnet50', 'se_resnet50_fc512', 
'se_resnet101', 'se_resnext50_32x4d', 'se_resnext101_32x4d', 'densenet121', 'densenet169', 
'densenet201', 'densenet161', 'densenet121_fc512', 'inceptionresnetv2', 'inceptionv4', 'xception', 'resnet50_ibn_a', 
'resnet50_ibn_b', 'nasnsetmobile', 'mobilenetv2_x1_0', 'mobilenetv2_x1_4', 'shufflenet', 'squeezenet1_0', 
'squeezenet1_0_fc512', 'squeezenet1_1', 'shufflenet_v2_x0_5', 'shufflenet_v2_x1_0', 'shufflenet_v2_x1_5', 
'shufflenet_v2_x2_0', 'mudeep', 'resnet50mid', 'hacnn', 'pcb_p6', 'pcb_p4', 'mlfn', 'osnet_x1_0', 'osnet_x0_75', 
'osnet_x0_5', 'osnet_x0_25', 'osnet_ibn_x1_0', 'osnet_ain_x1_0', 'osnet_ain_x0_75', 'osnet_ain_x0_5', 'osnet_ain_x0_25']"

A mí este error me salió porque puse el nombre del modelo con los pesos preentrenados. La variable model_name solo puede tener el nombre del modelo con el que se entrenó para obtener en este caso, los pesos preentrenados model.resnet50.pth.tar-20.



Yo usé, para empezar la primera iteración del flujo, el modelo de sportmot por defecto [sports_model.pth.tar-60](https://drive.google.com/file/d/1Wt_U-D2wfkMyKl1RIuIN2mAoM8M99jho/view?usp=sharing): 

.. code-block:: python
    python tools/demo.py 

Nota: 
   Modificar esta linea del codigo de demo.py para poner tu video como input: 
    parser.add_argument(
        "--path", default="../video2.mp4", help="path to images or video"
    )

Luego aplicar:
Usaremos vídeo2.mp4 que es un clip de largo de un partido de fútbol amateur.

.. code-block:: python
   python extract_frames.py --video_path video2.mp4 --output_dir frames_trackerVideo2

Crear una carpeta gt con el archivo MOT resultado de ejecutar demo.py con el video

.. code-block:: python
   python generate_tracklets.py --model_path "../reid_checkpoints/sports_model.pth.tar-60" --data_path "C:\Users\jismbs\Documents\gta-link\frames_trackerVideo2" --pred_dir "." --tracker "DeepEIoU"

Usé esta combinación de parámetros para la ejecución de refine_tracklets.py: --use_split --min_len 100 --eps 0.6 --min_samples 10 --max_k 3 --use_connect --spatial_factor 1.0 --merge_dist_thres 0.4
Es la más óptima en cuanto a resultados (comprobado por prueba y error), ya que es la que crea la menor cantidad de tracklets (menos cantidad de ids distintos)

.. code-block:: python
   python refine_tracklets.py --dataset SoccerNet --tracker DeepEIoU --track_src DeepEIoU_Tracklets_frames_trackerVideo2 --use_split --min_len 100 --eps 0.6 --min_samples 10 --max_k 3 --use_connect --spatial_factor 1.0 --merge_dist_thres 0.4

.. code-block:: python
   python visualize2.py  

.. code-block:: python
   python videomakerByFrame.py

### Segundo capítulo (etiquetado de dataset para reidentificación)

En este capítulo empezaremos por corregir el mot resultado de ejecutar refine_tracklets.py. Para ello hice dos programas que me ayudaban a semiautomatizar el proceso de corrección del fichero mot.

Uno para hacer cambios más generales (p. ej cambiar un id para el resto de la secuencia de vídeo). 
.. code-block:: python
   python annotate_review.py

Otro para hacer cambios más precisos frame a frame
.. code-block:: python
   python annotate_review_precise.py

Recomiendo encarecidamente que los ficheros se ejecuten varias veces y que no se haga todo directamente (p. ej hacer un único cambio de id por cada ejecución del annotate_review.py). Ya que es fácil equivocarse y tener que descartar el proceso de correción de 2h no es factible.

Tras varias correciones me quedé con el archivo que consideré suficientemente correcto como para tomarlo de referencia para entrenamiento y evaluación: [mot_corr30_c.txt](https://github.com/JuanSoM/TFG---Player-tracking-and-re-identification-in-amateur-football-using-object-detection/blob/main/code/gta-link%20-%20TFG/DeepEIoU_trackerVideo2_Split%2BConnect_eps0.8_minSamples10_K4_mergeDist0.7_spatial1.0/mot_corr30_c.txt)


Una vez tengamos el archivo mot casi perfecto ejecutaremos el siguiente programa con la intención de crear un directorio general y dentro de este, uno individual para cada uno de los jugadores detectados en el vídeo. El mot_file tiene que ser el corregido para poder tener el mejor entrenamiento y evaluación posible.

.. code-block:: python
   python dicMaker_idPlayer.py --mot_file "C:\Users\jismbs\Documents\gta-link\DeepEIoU_trackerVideo2_Split+Connect_eps0.8_minSamples10_K4_mergeDist0.7_spatial1.0\mot_corr30_c.txt" --image_folder "C:\Users\jismbs\Documents\gta-link\frames_trackerVideo2\video2\img1" --output_folder "C:\Users\jismbs\Documents\gta-link\player_crops"

Con el siguiente código tendremos un directorio general. Y luego varias subcarpetas divididas en train, query y gallery. Para poder entrenar el modelo de ReID (train) y poder evaluarlo más tarde (query y gallery)

.. code-block:: python
   python dicMakerForTrainingReID.py 

### Tercer capítulo (entrenamiento de un modelo con mi dataset etiquetado)

Para realizar el entrenamiento del modelo de ReID me base en la documentación de [Torchreid](https://kaiyangzhou.github.io/deep-person-reid/) proporcionado por el repositorio de [deep-person-reid](https://github.com/KaiyangZhou/deep-person-reid)

Bastaría con ejecutar la siguiente línea en el directorio de [entrenamientoReID](code/entrenamientoReID)

.. code-block:: python
   python main.py 

### Cuarto capítulo (evaluación de ReID)

Tendríamos que ejecutar la siguiente línea estando en el directorio de [entrenamientoReID](code/entrenamientoReID):

.. code-block:: python
   python eval.py 

### Quinto capítulo (vídeos generados con distintos modelos)

Sería repetir el capítulo uno, pero cambiando el model_name y los pesos usados (p. ej model.resnet50.pth.tar-20)
De esta manera iremos obteniendo vídeos diferentes usando un modelo distinto y podremos comparar los resultados de manera visual.


## Referencias

1. [Person Re-identification](https://paperswithcode.com/task/person-re-identification)
2. [SoccerNet](https://github.com/SoccerNet/sn-tracking)
3. [Sportsreid GitHub - shallowlearn](https://github.com/shallowlearn/sportsreid)
4. [Multi-object Tracking: A Review](https://sertiscorp.medium.com/multi-object-tracking-a-review-6aaeea495209)
5. [deep-person-reid](https://github.com/KaiyangZhou/deep-person-reid)
6. [torchreid doc](https://kaiyangzhou.github.io/deep-person-reid/)
7. ```bib
   @inproceedings{sun2024gta,
      title={GTA: Global Tracklet Association for Multi-Object Tracking in Sports},
      author={Sun, Jiacheng and Huang, Hsiang-Wei and Yang, Cheng-Yen and Hwang, Jenq-Neng},
      booktitle = {Proceedings of the Asian Conference on Computer Vision},
      pages = {421-434},
      year={2024},
      publisher = {Springer}
   }
8. ```bib
   @inproceedings{huang2024iterative,
      title={Iterative Scale-Up ExpansionIoU and Deep Features Association for Multi-Object Tracking in Sports},
      author={Huang, Hsiang-Wei and Yang, Cheng-Yen and Sun, Jiacheng and Kim, Pyong-Kun and Kim, Kwang-Ju and Lee, Kyoungoh and Huang, Chung-I and Hwang, Jenq-Neng},
      booktitle={Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision},
      pages={163--172},
      year={2024}
   }
## Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).
