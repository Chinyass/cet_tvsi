const snmp = require ("net-snmp");
class mySnmp{

    constructor(ip,community){
        this.ip = ip
        this.community = community
        this.session = snmp.createSession (ip, community);
    }

    async get(oids) {
        return await this.#getSession(oids) 
    }

    #getSession(oids) {
        let self = this
        return new Promise(function(resolve,reject){
            self.session.get (oids, function (error, varbinds) {
                if (error) {
                    reject(error);
                } else {
                    let data = []
                    for (var i = 0; i < varbinds.length; i++) {
                        if (snmp.isVarbindError (varbinds[i])) {
                            console.log(snmp.varbindError (varbinds[i]));
                        } else {
                            data.push(varbinds[i].value)
                        }
                    }
                    resolve(data)
                }
            });
        })
    }

    async getSubtree(OID){

        let self = this
        let final_result = [];
        function doneCb(error) {
            
            if (error)
                console.error("doneCb: Error:", error.toString());
       
        }

        function feedCb(varbinds) {
            for (var i = 0; i < varbinds.length; i++) {
                if (snmp.isVarbindError(varbinds[i]))
                console.error(snmp.varbindError(varbinds[i]));
                else {
                var snmp_rez = {
                    oid: (varbinds[i].oid).toString(),
                    value: (varbinds[i].value).toString()
                };

                final_result.push(snmp_rez);
                }
            }
        }

        function vlc_snmp(OID) {
            return new Promise((resolve,reject) => {
                self.session.subtree(OID, 20, feedCb, (error) => {
                    doneCb(error);
                    if (error) { 
                        reject(error);
                    } else { 
                        resolve(final_result);
                    }
                });
            });
        }
        
        return await vlc_snmp(OID);
    }





    #doneCb(error) {
        console.log("doneCb: final_result:", final_result);
        final_result = [];
        if (error)
          console.error("doneCb: Error:", error.toString());
      }
      
    #feedCb(varbinds) {
        console.log(this)
        for (var i = 0; i < varbinds.length; i++) {
          if (snmp.isVarbindError(varbinds[i]))
            console.error(snmp.varbindError(varbinds[i]));
          else {
            var snmp_rez = {
              oid: (varbinds[i].oid).toString(),
              value: (varbinds[i].value).toString()
            };
      
            final_result.push( snmp_rez )
          }
        }
      }

    #SubtreeSession(OID){
        let self = this
        let maxRepetitions = 20
        return new Promise((resolve,reject) => {
            self.session.subtree(OID, maxRepetitions, self.#feedCb, (error) => {
                // This is a wrapper callback on doneCb
                // Always call the doneCb
                self.#doneCb(error);
                if (error) { 
                    reject(error);
                } else { 
                    console.log( resolve() )
                }
            });
        });

    }

    
}

module.exports = mySnmp