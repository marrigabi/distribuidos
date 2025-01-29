import http from 'k6/http';

export const options = {
  stages: [
    { duration: '5s', target: 200 }, // ramp-up
    { duration: '20s', target: 200 }, // stable
    { duration: '5s', target: 0 }, // ramp-down 
  ],
};

export default () => {
  http.get('http://localhost:3000/?n1=3&n2=5');
};
