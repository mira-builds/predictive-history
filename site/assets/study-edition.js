(function () {
  function clearActive() {
    document.querySelectorAll(".outline-btn.active").forEach((el) => el.classList.remove("active"));
    document.querySelectorAll(".claim-card.active").forEach((el) => el.classList.remove("active"));
    document.querySelectorAll(".transcript-section.highlight").forEach((el) => el.classList.remove("highlight"));
  }

  function scrollToSlug(slug) {
    const target = document.getElementById(slug);
    if (!target) return;
    clearActive();
    target.classList.add("highlight");
    const btn = document.querySelector(`.outline-btn[data-slug="${slug}"]`);
    if (btn) btn.classList.add("active");
    target.scrollIntoView({ behavior: "smooth", block: "start" });
    if (slug === window.STUDY_PHASE1?.contrastSlug && window.STUDY_PHASE1?.focusClaim) {
      showClaimMorph(String(window.STUDY_PHASE1.focusClaim), false);
    }
  }

  function scrollToClaim(n, openMorph) {
    const claim = document.getElementById(`claim-${n}`);
    if (!claim) return;
    clearActive();
    claim.classList.add("active");
    if (openMorph !== false && document.getElementById("claim-morph-view")) {
      showClaimMorph(String(n), true);
    } else {
      claim.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
    const anchor = claim.getAttribute("data-anchor");
    if (anchor) scrollToSlug(anchor);
  }

  document.querySelectorAll(".outline-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const slug = btn.getAttribute("data-slug");
      if (slug) scrollToSlug(slug);
    });
  });

  document.querySelectorAll(".claim-marker, .claim-jump").forEach((btn) => {
    btn.addEventListener("click", (event) => {
      event.stopPropagation();
      const anchor = btn.getAttribute("data-anchor");
      const claim = btn.getAttribute("data-claim");
      if (claim) {
        scrollToClaim(claim);
        return;
      }
      if (anchor) scrollToSlug(anchor);
    });
  });

  document.querySelectorAll(".claim-card").forEach((card) => {
    card.addEventListener("click", () => {
      const n = card.getAttribute("data-claim");
      if (n) scrollToClaim(n);
    });
  });

  function loadClaimAids() {
    const node = document.getElementById("phase1-claim-aids");
    if (!node) return {};
    try {
      return JSON.parse(node.textContent || "{}");
    } catch (_err) {
      return {};
    }
  }

  const claimAids = loadClaimAids();
  const morphView = document.getElementById("claim-morph-view");
  const listView = document.getElementById("claims-list-view");

  function showClaimMorph(n, scrollNotes) {
    if (!morphView || !listView) return;
    const aid = claimAids[n];
    const card = document.getElementById(`claim-${n}`);
    if (!aid || !card) return;
    document.getElementById("claim-morph-n").textContent = `Claim ${n}`;
    document.getElementById("claim-morph-thesis").textContent = aid.thesis || "";
    const notices = document.getElementById("claim-morph-notices");
    notices.innerHTML = "";
    (aid.notices || []).forEach((line) => {
      const li = document.createElement("li");
      li.textContent = line;
      notices.appendChild(li);
    });
    const meta = card.querySelector(".claim-meta");
    document.getElementById("claim-morph-meta").textContent = meta ? meta.textContent : "";
    morphView.classList.remove("hidden");
    listView.classList.add("hidden");
    morphView.dataset.claim = n;
    morphView.dataset.anchor = card.getAttribute("data-anchor") || "";
    if (scrollNotes) {
      morphView.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
  }

  function hideClaimMorph() {
    if (!morphView || !listView) return;
    morphView.classList.add("hidden");
    listView.classList.remove("hidden");
  }

  document.getElementById("claim-morph-all")?.addEventListener("click", hideClaimMorph);
  document.getElementById("claim-morph-passage")?.addEventListener("click", () => {
    const anchor = morphView?.dataset.anchor;
    if (anchor) scrollToSlug(anchor);
  });
})();
