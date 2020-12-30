import axios from "axios";
import LocalStorageDataService from './services/LocalStorageDataService'

export var http = axios.create({
  baseURL: "http://localhost:8000/api",
  headers: {
    "Content-type": "application/json"
  },
});

export var httpAuth = axios.create({
  baseURL: "http://localhost:8000/api",
  headers: {
    "Content-type": "application/json",
    Authorization: `Bearer ${LocalStorageDataService.getAccessToken()}`
  },
});

export var httpAuthFiles = axios.create({
  baseURL: "http://localhost:8000/api",
  headers: {
    "Content-type": "multipart/form-data",
    Authorization: `Bearer ${LocalStorageDataService.getAccessToken()}`
  },
});