/* Keep Mermaid diagrams in sync with Material light/dark palette. */
(function () {
  function scheme() {
    return document.body.getAttribute("data-md-color-scheme") === "slate" ? "dark" : "default";
  }

  function mermaidTheme() {
    return scheme() === "dark" ? "dark" : "default";
  }

  function rerenderMermaid() {
    if (typeof mermaid === "undefined" || !mermaid.run) {
      return;
    }
    mermaid.initialize({
      startOnLoad: false,
      theme: mermaidTheme(),
      securityLevel: "loose",
    });
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

  var last = scheme();
  var observer = new MutationObserver(function () {
    var current = scheme();
    if (current === last) {
      return;
    }
    last = current;
    window.setTimeout(rerenderMermaid, 150);
  });

  document.addEventListener("DOMContentLoaded", function () {
    observer.observe(document.body, {
      attributes: true,
      attributeFilter: ["data-md-color-scheme"],
    });
  });
})();
