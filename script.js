// Aquesta funció s'executa automàticament en carregar la pàgina
async function carregarJocDelDia() {
    try {
        // 1. Busquem el fitxer JSON que ha generat el vostre script de Python
        const resposta = await fetch('dades_joc.json');
        const dades = await resposta.json();

        // 2. Posem el text de la variable 'original' al títol h2
        document.getElementById('frase-original').innerText = dades.original;

        // 3. Posem la traducció al paràgraf
        document.getElementById('frase-catala').innerText = dades.catala;

        // Podem guardar el país correcte en una variable global per comprovar-ho després
        console.log("El país a endevinar és: " + dades.pais_correcte);

    } catch (error) {
        console.error("Error carregant les dades del joc:", error);
        document.getElementById('frase-original').innerText = "No s'ha pogut carregar el joc d'avui.";
    }
}

carregarJocDelDia();