const cors = require('cors')
const express = require('express')
const app = express()
const http = require('http').createServer(app)

const io = require("socket.io")(http, {
    cors: {
      origin: "*",
    }
  });

const mySnmp = require('./mySnmp')
let rooms = []

io.on('connection', (socket) => {
    console.log('a user connected');
    socket.on("get-traffic", (serial) => {
        socket.join(serial)
    
        if (rooms.map( el => el.serial).includes(serial) ){
            const temp = []
            rooms.map( el => {
                if (el.serial == serial){
                    temp.push({
                        serial,
                        users: el.users.concat(socket.id)
                    })

                }
                else{
                    temp.push(el)
                }
            })
            rooms = [...temp]
        }
        else{
            console.log('room',serial,'created')
            rooms.push({
                serial,
                users: [socket.id]
            })
        }
    })
    socket.on("disconnect-traffic", () => {
        console.log('socket disconnect')
        rooms.forEach( el => {
            if (el.users.includes(socket.id) ){
                const index = el.users.indexOf(socket.id);
                el.users.splice(index, 1);
            }
        })
    });

});

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function sliceIntoChunks(arr, chunkSize) {
    const res = [];
    for (let i = 0; i < arr.length; i += chunkSize) {
        const chunk = arr.slice(i, i + chunkSize);
        res.push(chunk);
    }
    return res;
}

function convert_hex_to_dec(hexserial){
    hexserial = hexserial.replace('ELTX','454C5458')
    let arrhexserial = sliceIntoChunks(hexserial,2)
    return arrhexserial.map( el => parseInt(el, 16) ).join('.')
}

function getRandomArbitrary(min, max) {
    return Math.random() * (max - min) + min;
  }

setInterval(() => {
    rooms = rooms.filter( el => {
        el.users = [...new Set(el.users)]
        return el.users.length > 0 
    })
    console.log(rooms)
    rooms.forEach( async (room) => {
        
        console.log('sending data to ',room)
        let snmp = new mySnmp('10.3.0.35','private_set')
        
        const dec_serial = convert_hex_to_dec(room.serial)
        let old_data = 0
        try{
            const getRx = async () => {
                return await snmp.get([`1.3.6.1.4.1.35265.1.22.3.3.10.1.6.1.8.${dec_serial}.1.1`])
            }
            old_data = await getRx()
            const starttime = Math.ceil(Date.now() / 1000)
            await sleep(12000)
            let new_data = await getRx()
            const endtime = Math.ceil(Date.now() / 1000)
            rx = parseInt( ( ( parseInt(new_data) - parseInt(old_data) ) /  ( endtime - starttime  ) ) * 8 )
            
            //let rx = getRandomArbitrary(0,Math.pow(10,7))
            io.to(room.serial).emit("send_traffic",rx)
        }      
        catch (err){
            io.to(room.serial).emit("send_traffic",0)
        }
        
    })    
},13000)


http.listen(8002, () => {
    console.log('socket io server started 8002 port')
})