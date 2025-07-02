// 场馆相关功能
document.addEventListener('DOMContentLoaded', function() {
    // 获取场馆列表
    if (document.querySelector('.venue-list-container')) {
        loadVenues();
    }
});

function loadVenues() {
    const container = document.querySelector('.venue-list-container');
    container.innerHTML = '<div class="text-center py-5">加载中...</div>';

    fetch('/api/venues/')
        .then(response => {
            if (!response.ok) {
                throw new Error('获取场馆列表失败');
            }
            return response.json();
        })
        .then(venues => {
            renderVenues(venues);
        })
        .catch(error => {
            container.innerHTML = `<div class="alert alert-danger">${error.message}</div>`;
        });
}

function renderVenues(venues) {
    const container = document.querySelector('.venue-list-container');
    let html = '<div class="row">';

    venues.forEach(venue => {
        html += `
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="card h-100">
                <img src="${venue.image_url || '/images/placeholder.jpg'}" class="card-img-top" alt="${venue.name}">
                <div class="card-body">
                    <h5 class="card-title">${venue.name}</h5>
                    <p class="card-text">
                        <span class="badge bg-info">容量: ${venue.capacity}人</span>
                        <span class="badge bg-success ms-2">${venue.type}</span>
                    </p>
                    <a href="/venues/${venue.id}" class="btn btn-primary">查看档期</a>
                </div>
            </div>
        </div>
        `;
    });

    html += '</div>';
    container.innerHTML = html;
}
