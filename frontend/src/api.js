import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const chatWithStore = async (storeName, message) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/chat/${storeName}`, {
            message: message,
        });
        return response.data;
    } catch (error) {
        console.error("Error chatting with store:", error);
        throw error;
    }
};


