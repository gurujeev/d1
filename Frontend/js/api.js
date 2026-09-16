const API_BASE = "/api";


async function apiRequest(
    endpoint,
    options = {}
) {

    const token =
        localStorage.getItem("access_token");

    const headers = {
        ...(options.headers || {})
    };


    if (!(options.body instanceof FormData)) {

        headers["Content-Type"] =
            "application/json";
    }


    if (token) {

        headers["Authorization"] =
            `Bearer ${token}`;
    }


    const response =
        await fetch(
            `${API_BASE}${endpoint}`,
            {
                ...options,
                headers
            }
        );


    let data = {};

    try {

        data = await response.json();

    } catch {

        data = {};
    }


    if (!response.ok) {

        const message =
            data.detail ||
            "Something went wrong.";

        throw new Error(message);
    }


    return data;
}