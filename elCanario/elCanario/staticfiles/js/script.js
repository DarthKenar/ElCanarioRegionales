document.addEventListener('click', (e) => {
    if (e.target.nodeName == 'BUTTON' || e.target.nodeName == 'svg' || e.target.nodeName == 'line' ){
        e.target.closest('div').classList.add('vanish')
    }
})