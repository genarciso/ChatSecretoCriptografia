<h1>ChatSecretoCriptografia</h1>
<p>Chat desenvolvido para a disciplina de Segurança de Redes. Ele utiliza o protocolo TCP para a troca de mensagens e, inicialmente, troca as mensagens sem criptografia alguma. Dois algoritmos de cifragem foram utilizados: S-DES e RC4.
<h2>Modo de usar</h2>
<h3> Iniciando uma conversa:</h2>
<ol>
    <li>Inicie o servidor da seguinte maneira: $ python2 server.py [IP] [PORTA] (Exemplo: $ python2 server.py 127.0.0.1 5354)</li>
    <li>Inicie os clientes, em terminais distintos, da seguinte maneira: $ python3 client.py [IP] [PORTA]. Sendo o IP o mesmo do servidor e a porta também.</li>
    <li>Comece a trocar as mensagens.</li>
</ol>
<h3>Trocando a cifragem</h3>
<ul>
    <li>Em um terminal cliente digite: \crypt [rc4 | s-des | qualquer coisa]</li>
    <li>No outro terminal cliente, envie uma mensagem confirmando. Esta mensagem pode ser um 'Ok', ou qualquer coisa, só para o emissor do \crypt saber realmente que o usuário trocou a cifragem.
</ul>
<p>Se o usuário escolher s-des, então o método de cifragem será do S-DES. O mesmo acontecerá com o RC4.
<p>Se o usuário digitar qualquer outra coisa após o \crypt, então o os clientes passarão a conversar de maneira não cifrada.
<h2>Autores</h2>
<p> Aroldo Felix Pereira Junior (junioraroldo37@gmail.com)
<p> Gabriel Estevam Narciso (gabriel.estevam.narciso@gmail.com)
<h2>Referências</h2>

<b>Chat</b> : <a>https://github.com/dvatsav/Chat-Room-server</a>