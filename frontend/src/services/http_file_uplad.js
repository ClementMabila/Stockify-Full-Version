// services/http.js
import { getCSRFToken } from '../store/auth'

export default {
  async post(url, data) {
  let body;
  let headers = {
    'X-CSRFToken': getCSRFToken(),
  };

  // If already FormData, use as-is
  if (data instanceof FormData) {
    body = data;
    // Let browser set proper boundary automatically — don't set Content-Type
  } else {
    body = new FormData();
    for (let key in data) {
      if (data.hasOwnProperty(key)) {
        body.append(key, data[key]);
      }
    }
  }

  const response = await fetch(`http://localhost:8000${url}`, {
    method: 'POST',
    headers,
    credentials: 'include',
    body: body
  });

  if (!response.ok) throw new Error(await response.text());
  return response.json();
},
  async patch(url, data) {
    const response = await fetch(`http://localhost:8000${url}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      },
      credentials: 'include',
      body: JSON.stringify(data)
    });

    if (!response.ok) throw new Error(await response.text());
    return response.json();
  }
}