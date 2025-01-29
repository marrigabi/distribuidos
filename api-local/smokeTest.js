import http from 'k6/http';

export const options = {
  vus: 5,  // Número de usuários virtuais
  duration: '10s'  // Duração do teste
};

export default () => {
  http.get('http://localhost:3000/?n1=3&n2=5');
};
