import { SnackbarProvider } from "notistack";
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./style/index.css";
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <SnackbarProvider maxSnack={3}>
      <App />
    </SnackbarProvider>
  </React.StrictMode>
);
