import dotenv from "dotenv";
import express from 'express' 
import swaggerUi from 'swagger-ui-express';
import YAML from 'yamljs';
import path from 'path';
import cors from 'cors'; // cors 임포트 추가

const __dirname = path.dirname(new URL(import.meta.url).pathname);
const swaggerSpec = YAML.load('./swagger.yaml'); // 경로를 확인해주세요
const swaggerPath = '/Users/jihyun/Desktop/%EC%A1%B8%ED%94%84_%EC%BB%B4%EC%84%B8%EB%A7%88%EB%A6%AC/FOREST/2024-capston/swagger.yaml';

dotenv.config();

const app = express()
const port = process.env.PORT;
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));


app.use(cors()); 
app.use(express.static('public'));
app.use(express.json());
app.use(express.urlencoded({ extended: false })); 

app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})