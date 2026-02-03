
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 20 },
    { duration: '1m30s', target: 10 },
    { duration: '20s', target: 0 },
  ],
};

const API_BASE_URL = 'http://192.168.2.0';

export default function () {
  // Get random quote
  let res = http.get(`${API_BASE_URL}/quotes`);
  check(res, { 'status was 200': (r) => r.status == 200 });
  sleep(1);

  // Get all quotes
  res = http.get(`${API_BASE_URL}/quotes/all`);
  check(res, { 'status was 200': (r) => r.status == 200 });
  sleep(1);

  // Create a new user and get a token
  const user = {
    username: `user${__VU}@test.com`,
    password: 'password',
  };

  res = http.post(`${API_BASE_URL}/users/`, JSON.stringify(user), {
    headers: { 'Content-Type': 'application/json' },
  });
  check(res, { 'status was 200': (r) => r.status == 200 });


  const loginData = {
    username: user.username,
    password: user.password,
  };

  res = http.post(`${API_BASE_URL}/token`, loginData);

  let token = null;
  if (res.status === 200) {
    token = res.json('access_token');
  }

  if (token) {
    // Create a new quote
    const quote = {
      author: 'K6',
      quote: 'This is a test quote',
    };

    const headers = {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    };

    res = http.post(`${API_BASE_URL}/quotes`, JSON.stringify(quote), { headers });
    check(res, { 'status was 201': (r) => r.status == 201 });
    sleep(1);
  }
}
