import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  config.withCredentials = true; // Barcha so‘rovlarga qo‘shildi
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401 && error.config && !error.config._retry) {
      error.config._retry = true;
      try {
        const refresh = localStorage.getItem("refresh_token");
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/token/refresh/`, { refresh });
        const newAccessToken = response.data.access;
        localStorage.setItem("access_token", newAccessToken);
        error.config.headers.Authorization = `Bearer ${newAccessToken}`;
        return api(error.config);
      } catch (refreshError) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default api;