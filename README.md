# TournamentStreamHelper

A rewrite of joaorb64/TournamentStreamHelper into React and FastAPI (via Python with asyncio). May change a _lot_ with things getting started.

It's recommended to install Node.js (for NPM) and Python 3, then run `npm run setup` (`npm run setup:win` on Windows) to install Python dependencies and `npm install` to install JavaScript dependencies.

`npm run dev` (`npm run dev:win` on Windows) to run the developer environment with hot-module reloading.

`npm run server` (`npm run server:win` on Windows) to run the server only and not compile the frontend.

`npm run build` to compile the frontend for use by FastAPI.

The following dependencies are planned to be used in Python:

- [FastAPI](https://fastapi.tiangolo.com/) for server-side rendering and REST APIs
- [uvicorn](https://www.uvicorn.org/) as the ASGI server
- [httpx](https://www.python-httpx.org/async/) for asyncio web requests
- [loguru](https://github.com/Delgan/loguru) for logging
- [socketio](https://python-socketio.readthedocs.io/en/stable/server.html#uvicorn-daphne-and-other-asgi-servers) for communication to/from React

...and in React:

- React 18
- [Material UI](https://mui.com/material-ui/all-components/)
- [react-router](https://reactrouter.com/en/main/start/overview)
- [react-intl](https://formatjs.io/docs/react-intl/) for i18n
- [react-use-websocket](https://github.com/robtaussig/react-use-websocket?tab=readme-ov-file#getting-started) for Socket.io support
- [zustand](https://github.com/pmndrs/zustand) for state management