import { check, sleep } from 'k6';
import http from 'k6/http';

export const options = {
  vus: 10, // Number of virtual users (concurrent users)
  duration: '30s', 
};

export default function () {
  const url = 'http://localhost:8000/api/urls/shorten';
  const payload = JSON.stringify({
    original_url: 'https://example.com',
    custom_code: '', 
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  
  const response = http.post(url, payload, params);


  check(response, {
    'status is 201': (r) => r.status === 201,
    'response has short_url': (r) => r.json('short_url') !== undefined,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1);
} 