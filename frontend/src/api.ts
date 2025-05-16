import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL, // To‘g‘ri o‘zgaruvchi
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  } else {
    console.warn("Access token topilmadi, so‘rov autentifikatsiz yuborilmoqda");
  }
  config.withCredentials = true; // Credentials uchun zarur
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401 && error.config && !error.config._retry) {
      error.config._retry = true;
      try {
        const refresh = localStorage.getItem("refresh_token");
        if (!refresh) {
          throw new Error("Refresh token mavjud emas");
        }
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/auth/token/refresh/`, { refresh });
        const newAccessToken = response.data.access;
        localStorage.setItem("access_token", newAccessToken);
        error.config.headers.Authorization = `Bearer ${newAccessToken}`;
        return api(error.config);
      } catch (refreshError: any) {
        console.error("Refresh token xatosi:", refreshError.response?.data || refreshError.message);
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }
    console.error("API xatosi:", {
      status: error.response?.status,
      data: error.response?.data,
      message: error.message,
    }); // Xatolarni batafsil log qilish
    return Promise.reject(error);
  }
);

export default api;