/* Re-render Mermaid diagrams when the user toggles light/dark mode. */
(function () {
  function currentScheme() {
    return document.body.getAttribute("data-md-color-scheme") || "default";
  }

  function rerenderMermaid() {
    if (typeof mermaid === "undefined" || !mermaid.run) {
      return;
    }
    var nodes = document.querySelectorAll(".mermaid");
    if (!nodes.length) {
      return;
    }
    nodes.forEach(function (node) {
      if (node.getAttribute("data-processed") === "true") {
        var code = node.querySelector("code");
        if (code) {
          node.removeAttribute("data-processed");
          node.innerHTML = code.textContent;
        }
      }
    });
    mermaid.run({ nodes: nodes });
  }

  var lastScheme = currentScheme();
  var observer = new MutationObserver(function () {
    var scheme = currentScheme();
    if (scheme === lastScheme) {
      return;
    }
    lastScheme = scheme;
    window.setTimeout(rerenderMermaid, 120);
  });

  observer.observe(document.body, {
    attributes: true,
    attributeFilter: ["data-md-color-scheme"],
  });
})();
