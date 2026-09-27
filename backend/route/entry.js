import express from 'express';
import { getEntries } from '../service/entry.js';

const router = express.Router();

router.get('/entries', async (req, res) => {
    const user = req.query.user
    if(!user){
        return res.status(400).json("error: 参数必填")
    }
    try{
        const entries = await getEntries(user);
        res.json(entries);
    } catch(err) {
        res.status(500).json("error: 服务器内部错误")
        console.log(err)
    }

})

export default router;