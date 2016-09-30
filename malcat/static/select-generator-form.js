let $selectGeneratorForm = $('#select-generator')

$selectGeneratorForm.submit(event => {
  event.preventDefault()
  let username = $selectGeneratorForm.children('[name="username"]').val(),
      listType = $selectGeneratorForm.children('[name="list-type"]').val(),
      generator = $selectGeneratorForm.children('[name="generator"]').val()
  let generatorHref = generator.toLowerCase() + '?' + $.param({
    user: username,
    list: listType
  })
  window.location.href = generatorHref
})
