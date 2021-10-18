HitchGlobals = {
    handlers: {},
    callbacks: {}
}

class HitchClient
{
    constructor(socketUri)
    {

        // The Websocket Object
        this.websocket  = new WebSocket(socketUri);

        // HitchGlobals.handlers = { name: function, name: function, ...}
        // HitchGlobals.callbacks[data.id] = (data) => {...}

        // Send
        this.send       = (action, data, callback=undefined) => {
            data.action = action;
            data.id     = Date.now().toString();
            
            data.hasCallback = false;
            // Sets callback if "callback" is passed through keyword.
            // This allows us to define how to handle the response to each message, if needed.
            if (callback != undefined) {
                HitchGlobals.callbacks[data.id] = callback;
                data.hasCallback = true;
            }
            this.websocket.send(JSON.stringify(data));
        };

        // Adds a handler to the self.handlers object.
        this.addHandler = (actionName, handlerFunction) => {
            HitchGlobals.handlers[actionName] = handlerFunction
        };

        this.websocket.onmessage = function (event){

            let data = JSON.parse(event.data);

            // Handles Callbacks that were passed through the this.send(*, hasCallback = true) method.
            if ('hasCallback' in data && 'id' in data && data.id in HitchGlobals.callbacks && data.hasCallback){
                HitchGlobals.callbacks[data.id](data, this.websocket);
                delete HitchGlobals.callbacks[data.id];
            }

            // Handles Handlers that were defined using this.addHandler.
            else if ('action' in data)// && 'id' in data)
            {
                for ( let [action, handler] of Object.entries(HitchGlobals.handlers) )
                {
                    if (action == data.action){
                        handler(data, this.websocket)
                    }
                }
            }
        }

        this.websocket.onclose = (event) => {
            console.log(event);
            alert("Hitch Socket Error: Connection to backend was lost or cannot be created.");
        };

        this.websocket.onopen = () => {
            console.log("⚡ by Hitch Socket Framework!");
        };
    }

}













