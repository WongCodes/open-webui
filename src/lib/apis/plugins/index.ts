import { WEBUI_API_BASE_URL } from '$lib/constants';

export const getPlugins = async (token: string) => {
    let error = null;
    const res = await fetch(`${WEBUI_API_BASE_URL}/plugins/`, {
        method: 'GET',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
            authorization: `Bearer ${token}`
        }
    })
        .then(async (res) => {
            if (!res.ok) throw await res.json();
            return res.json();
        })
        .catch((err) => {
            error = err.detail || err;
            console.error(err);
            return null;
        });
    if (error) throw error;
    return res;
};

export const getPluginConfig = async (token: string, name: string) => {
    let error = null;
    const res = await fetch(`${WEBUI_API_BASE_URL}/plugins/${name}/config`, {
        method: 'GET',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
            authorization: `Bearer ${token}`
        }
    })
        .then(async (res) => {
            if (!res.ok) throw await res.json();
            return res.json();
        })
        .catch((err) => {
            error = err.detail || err;
            console.error(err);
            return null;
        });
    if (error) throw error;
    return res;
};

export const setPluginConfig = async (token: string, name: string, config: object) => {
    let error = null;
    const res = await fetch(`${WEBUI_API_BASE_URL}/plugins/${name}/config`, {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
            authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ config })
    })
        .then(async (res) => {
            if (!res.ok) throw await res.json();
            return res.json();
        })
        .catch((err) => {
            error = err.detail || err;
            console.error(err);
            return null;
        });
    if (error) throw error;
    return res;
};
