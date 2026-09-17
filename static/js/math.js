document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.math-expression').forEach(element => {
    katex.render(element.textContent, element, {
      displayMode: element.dataset.display === 'true',
      throwOnError: false,
      trust: false,
      strict: 'ignore'
    });
  });
});
