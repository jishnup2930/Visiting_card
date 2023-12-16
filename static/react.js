import React from "react";
import EmployeeDetails from "./site.js";




// 'use strict';

//         function Like() {
//             const [text, setText] = React.useState('');
//             const [state, setState] = React.useState([]);

//             const addItem = () => {
//                 if (!text) return;
//                 setState((s) => [...s, { id: s.length, text: text }]);
//                 setText('');
//             };

//             console.log(state);

//             return (
//                 <div>
//                     <h1>Leave Management</h1>
//                     Enter text: <input type="text" value={text} onChange={(e) => setText(e.target.value)} /><br/>
//                     <button onClick={addItem}>Add</button>
//                     <ul>
//                         {state.map(({ id, text }) => <li key={id}>{text}</li>)}
//                     </ul>
//                 </div>
//             );
//         }

//         const domContainer = document.getElementById('root');
//         const root = ReactDOM.createRoot(domContainer);
//         root.render(React.createElement(Like));
