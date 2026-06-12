import { createElement, useRef, useState } from "react";

function App() {

  function handleAdd(e) {
    e.preventDefault();
    const input = document.getElementById("user");
    const v = input.value.trim();
    if (!v) return;
     const ul = document.getElementById("items");
    const p = document.createElement("p"); // cria a tag <p>
    p.className = "user";                  // adiciona a classe
    p.textContent = v;                     // define o texto
    ul.appendChild(p);                     // insere no DOM
    input.value = "";
  }




  const Raeadchat = () => {
    const novochat = [...Chat]
    novochat.push("novamensagem")
    setChat(novochat)
    console.log(novochat)
  }



  /* mercado */
  //const listamercado = ["banana", "maçã", "laranja", "uva"];
  const [listamercado, setListamercado] = useState([]);


  const addinput = useRef();
  console.log(addinput.current)
  //hook
  //useState - cria uma variavel estado
  // ele não retorna uma informação
  //ele retorna um array [a variavel que armazena a informação, uma função para alterar essa variavel ]

  /* useref */

  const additem = () => {
    const novalista = [...listamercado]
    const valorinput = addinput.current.value;

    if (valorinput) {
      novalista.push(valorinput)
      addinput.current.value = "";
    }
    console.log(novalista)

    setListamercado(novalista)
    //const listamecado = novalista
  }
  /* mercado */


  return (
    <>
        {/* input */}
         
      {/* totem */}
      <div className="totem" >
        <button className="button_totem" onClick={() => {
          const chatbox = document.getElementById('chatbox');
          if (chatbox.style.display === "none" || chatbox.style.display === "") {
            chatbox.style.display = "flex"; // abre
          } else {
            chatbox.style.display = "none"; // fecha
          }
        }}> <img src="src/assets/Agente Nicole(1).png" alt="totem" /> </button>
      </div>
      {/* chatbox */}
      <div className="chatbox" hidden id="chatbox" style={{ display: "none" }}>
        <div className="chat" id="items">

          <p className="nicole">Olá, eu sou a Nicole, sua assistente virtual. Como posso ajudar você hoje?</p>

          <agent />
        </div >
        <div className="user_chat">
          <form onSubmit={handleAdd}>
            <div>
              <input id="user" type="text" placeholder="digete sua mensagem" autoComplete="off" />
              <button type="submit">Enviar</button>
              <button id="botao-mic" className="btn-microfone" >🎙️</button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
}

export default App
