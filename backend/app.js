import express from 'express';
import entryRouter from './route/entry.js';

const app = express();
const PORT = 3000

app.use(express.json())
app.use('/api', entryRouter)
app.use((err, req, res, next) => {
  console.error(err)
  res.status(500).json({ error: '服务器内部错误' })
})

app.listen(PORT, () => {console.log(`Server running at http://localhost:${PORT}`)})