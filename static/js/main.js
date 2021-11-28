let search_form = document.getElementById('search_form')
let page_links = document.getElementsByClassName('page-link')

// TODO: keep search form exists
if (search_form) {
    for (let i = 0; i < page_links.length; i++) {
        page_links[i].addEventListener('click', function (e) {
            e.preventDefault()
            // TODO: get data attributes
            let page = this.dataset.page

            // TODO: add search input to form
            search_form.innerHTML += `<input value=${page} name="page" hidden/>`
            search_form.submit()
        })
    }
}
