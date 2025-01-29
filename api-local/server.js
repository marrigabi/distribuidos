const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  const n1 = parseInt(req.query.n1, 10); // Converte o parâmetro para número
  const n2 = parseInt(req.query.n2, 10); // Converte o parâmetro para número

  // Verifica se os parâmetros são números válidos
  if (isNaN(n1) || isNaN(n2)) {
    return res.status(400).send('Parâmetros n1 e n2 devem ser números válidos.');
  }

  const result = n1 + n2;
  res.send(`Resultado da soma: ${result}`);
});

app.listen(port, () => {
  console.log(`API rodando em http://localhost:${port}`);
});
