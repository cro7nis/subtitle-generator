# Subtitle generator API and UI

Subtitle generator with [faster whisper](https://github.com/SYSTRAN/faster-whisper), which is a
reimplementation of  [OpenAI's Whisper](https://github.com/openai/whispermodel) using CTranslate2 for faster inference.

The Subtible generator consists of an API that is built with [FastAPI](https://fastapi.tiangolo.com/) and a
with [Streamlit](https://streamlit.io/) UI.

## Docker

- Build the API

   ```
   docker build . -f docker/service.Dockerfile -t <service-image-name>
   ```

- Build the UI

   ```
   docker build . -f docker/ui.Dockerfile -t <ui-image-name>
   ```

- Run the API

   ```
   docker run --gpus '"device=<device-id>"' -e DYNACONF_API__SERVER__BIND=<port> --network host --gpus all <service-image-name>
   
   ```
  
  - `<device-id>` the gpu id
  - `<port>` the API port (default: 8050)


- Run the UI

   ```
   docker run --network host -e PORT=<ui-port> -e DYNACONF_API__HOST=<api-host> -e DYNACONF_API__PORT=<api-port> <ui-image-name>
   ```

  -   `<port>` the UI port (default: 8051)
  -   `<api-host>` the host address (default: localhost)
  -   `<api-port>` the UI port  (default: 8050)


<hr>

## Docker compose

- Deploy API and UI

```
docker-compose -f docker/docker-compose.yml up 
```


<hr>

## API documentation

```    
http://<api-host>:<api-port>/subtitle/api/v1/docs
```