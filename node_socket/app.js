const io = require("socket.io")(3000,{
    cors: {
        origin: "*",
    }
})
const mySnmp = require('./mySnmp')

let rooms = []

io.on('connection', (socket) => {
    console.log('a user connected');
    socket.on("get-traffic", (serial) => {
        console.log(serial)
        socket.join(serial)

        if (rooms.map( el => el.serial).includes(serial) ){
            console.log("FINDED")
            const temp = []
            rooms.map( el => {
                if (el.serial == serial){
                    temp.push({
                        serial,
                        users: el.users + 1
                    })
                }
                else{
                    temp.push(el)
                }
            })
            rooms = [...temp]
        }
        else{
            console.log("NOT FOUND")
            rooms.push({
                serial,
                users: 1
            })
        }
        
    })
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
    //arrhexserial = arrhexserial.map( el => el.join('') )
    return arrhexserial.map( el => parseInt(el, 16) ).join('.')
}


setInterval(() => {
    rooms.forEach( async (room) => {
        let snmp = new mySnmp('10.3.0.35','private_set')
        const dec_serial = convert_hex_to_dec(room.serial)
        console.log(dec_serial)        
        const getRx = async () => {
            return await snmp.get([`1.3.6.1.4.1.35265.1.22.3.3.10.1.6.1.8.${dec_serial}.1.1`])
        }
        let old_data = await getRx()
        const starttime = Math.ceil(Date.now() / 1000)
        await sleep(12000)
        let new_data = await getRx()
        const endtime = Math.ceil(Date.now() / 1000)
        rx = parseInt( ( ( parseInt(new_data) - parseInt(old_data) ) /  ( endtime - starttime  ) ) * 8 )
        console.log('RX',rx)
        io.to(room.serial).emit("send-traffic",rx)
    })    
},13000)
