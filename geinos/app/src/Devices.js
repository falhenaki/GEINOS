import React, { Component } from 'react';
import './Devices.css';
var stuff=[]
var id=''
class Devices extends Component {
    constructor() {
        super();
        this.state = { items: [] };
    }


    componentDidMount() {
        fetch(`https://jsonplaceholder.typicode.com/posts/1`)
            .then(result=> result.json()).then((items) => {
               // console.log(items);
              //  console.log(items.length);
                this.setState({items: items});
                stuff=items;
                console.log(stuff);
            }
            );
    }

    render() {
        const data = stuff;
        return (
            <div>
                {data.map(function(d, idx){
                    return (<li key={idx}>{d.title}</li>)
                })}
            </div>
        );
    }
}

export default Devices;