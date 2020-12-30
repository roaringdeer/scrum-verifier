import http from "../http-common";

class DatabaseDataService {
  getAll() {
    return http.get("/database");
  }

  get(id) {
    return http.get(`/database/${id}`);
  }

  create(data) {
    return http.post("/database/", data);
  }

  update(id, data) {
    return http.put(`/database/${id}`, data);
  }

  delete(id) {
    return http.delete(`/database/${id}`);
  }

  deleteAll() {
    return http.delete(`/database`);
  }

  findByTitle(title) {
    return http.get(`/database?title=${title}`);
  }
}

export default new DatabaseDataService();