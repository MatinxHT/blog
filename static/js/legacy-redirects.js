// Preserve WordPress query-string permalinks when they reach this site's home.
const postId = new URLSearchParams(window.location.search).get('p');
const migratedIds = ['100001', '100002', '100003', '100004', '100005', '100006', '100007', '100008', '100009', '100010', '100011', '100012', '100028'];
if (migratedIds.includes(postId)) {
  window.location.replace(new URL(`posts/wp-${postId}/${window.location.hash}`, document.querySelector('link[rel="canonical"]').href));
}
