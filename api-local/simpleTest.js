import http from 'k6/http';

export default () => {
  http.get('http://localhost:3000/?n1=10&n2=20');
};
