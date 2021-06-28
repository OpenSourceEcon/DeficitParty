PARTY_CONTROL_CALLBACK="""
var button = radio.active;
console.log("--Running JS Callback--");

if (button == '0') {
    var source = deficit_cds.data;
    for (var i=0; i < source.x.length; i++) {
        if(source.demSenateSeats[i]>50 && source.demHouseSeats[i]>217 && source.demWhiteHouse[i]==1 ) 
        { 
            source.color[i]='blue'; 
        }
        else if(source.demSenateSeats[i]<50 && source.demHouseSeats[i]<217 && source.demWhiteHouse[i]==0)
        { 
            source.color[i]='red'; 
        }
        else
        { 
            source.color[i]='green' 
        }
    }
    deficit_cds.change.emit();
}
if (button == '1') {
    var source = deficit_cds.data;
    for (var i=0; i < source.x.length; i++) {
        if(source.demSenateSeats[i]>50 && source.demWhiteHouse[i]==1 ) 
        { 
            source.color[i]='blue'; 
        }
        else if(source.demSenateSeats[i]<50 && source.demWhiteHouse[i]==0)
        { 
            source.color[i]='red'; 
        }
        else
        { 
            source.color[i]='green' 
        }
    }
    deficit_cds.change.emit();
}
if (button == '2') {
    var source = deficit_cds.data;
    for (var i=0; i < source.x.length; i++) {
        if(source.demHouseSeats[i]>217 && source.demWhiteHouse[i]==1 ) 
        { 
            source.color[i]='blue'; 
        }
        else if(source.demHouseSeats[i]<217 &&source.demWhiteHouse[i]==0)
        { 
            source.color[i]='red'; 
        }
        else
        { 
            source.color[i]='green' 
        }
    }
    deficit_cds.change.emit();
}
"""