const API_URL = "http://127.0.0.1:8000";

type RequestOptions = {
    method?: string;
    headers?: Record<string, string>;
    body?: any;
};

export async function apiRequest(endpoint: string, options: RequestOptions = {}) {
    const { method = "GET", headers = {}, body } = options;

    // 1. Auto-inject token if user is logged in
    const token = typeof window !== 'undefined' ? localStorage.getItem("access_token") : null;
    console.log("JWT TOKEN:", token);
    const authHeaders: Record<string, string> = token
        ? { "Authorization": `Bearer ${token}` }
        : {};

    const config: RequestInit = {
        method,
        headers: {
            "Content-Type": "application/json",
            ...authHeaders, // Inject Auth
            ...headers,     // Allow overrides
        },
    };

    if (body) {
        config.body = JSON.stringify(body);
    }

    // Log API call (simplified for noise reduction)
    // console.log(`[API] ${method} ${API_URL}${endpoint}`);

    try {
        const response = await fetch(`${API_URL}${endpoint}`, config);

        // 2. Global 401 Handler (Token Expired / Invalid)
        if (response.status === 401) {
            if (typeof window !== 'undefined') {
                console.warn("[API] 401 Unauthorized - Redirecting to login");
                localStorage.removeItem("access_token");
                window.location.href = "/login";
                return; // Stop execution
            }
        }

        const contentType = response.headers.get("content-type");
        let data;
        if (contentType && contentType.indexOf("application/json") !== -1) {
            data = await response.json();
        } else {
            data = await response.text();
        }

        if (!response.ok) {
            const errorMessage = (data && typeof data === 'object' && data.detail)
                ? data.detail
                : (typeof data === 'string' ? data : "An unexpected error occurred");
            throw new Error(errorMessage);
        }

        return data;
    } catch (error) {
        console.error(`[API ERROR]`, error);
        throw error;
    }
}
