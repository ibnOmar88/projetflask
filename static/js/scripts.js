

const carteModal= document.querySelector('#exampleModal1')

carteModal.addEventListener('show.bs.modal', function(event){
     const btn= event.relatedTarget
     const iduser= btn.getAttribute('data-user-id')
     document.querySelector('#modal-user-id').value=iduser
})