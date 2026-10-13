/**
 * LogicLab Academy Controller
 * Renders structured problem-solving masterclasses and provides interactive practice launchers.
 */
class AcademyController {
    constructor(containerElement, onPracticeCallback) {
        this.container = containerElement;
        this.onPractice = onPracticeCallback;
        this.topics = [];
        this.selectedTopic = null;

        this.init();
    }

    async init() {
        try {
            const res = await fetch('/api/academy/topics');
            const data = await res.json();
            this.topics = data.topics || [];
            this.render();
        } catch (e) {
            console.error('Failed to load academy topics', e);
        }
    }

    render() {
        this.container.innerHTML = `
            <div class="academy-hero">
                <div class="academy-hero-text">
                    <h2><span class="icon">🎓</span> LogicLab Academy</h2>
                    <p>Master formal deduction methods, finite difference calculations, and progressive pattern recognition from first principles.</p>
                </div>
            </div>

            <div class="academy-topics-grid">
                ${this.topics.map(topic => `
                    <div class="academy-card" data-topic-id="${topic.id}">
                        <div class="academy-card-header">
                            <span class="topic-category-badge">${topic.category}</span>
                            <span class="topic-read-time">${topic.read_time}</span>
                        </div>
                        <h3 class="topic-title">${topic.title}</h3>
                        <p class="topic-summary">${topic.summary}</p>
                        <div class="academy-card-footer">
                            <button type="button" class="btn-read-lesson" data-topic-id="${topic.id}">
                                Read Masterclass &rarr;
                            </button>
                        </div>
                    </div>
                `).join('')}
            </div>

            <!-- Masterclass Reader Modal -->
            <div class="modal-overlay hidden" id="academy-modal">
                <div class="modal-content academy-modal-content">
                    <div class="modal-header">
                        <div class="modal-header-titles">
                            <span class="topic-category-badge" id="modal-category-badge">Category</span>
                            <h3 id="modal-topic-title">Topic Title</h3>
                        </div>
                        <button type="button" class="btn-modal-close" id="btn-close-academy">&times;</button>
                    </div>
                    <div class="modal-body" id="modal-topic-body">
                        <!-- Sections injected here -->
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn-primary" id="btn-modal-practice">
                            <span class="icon">🚀</span> Practice This Technique Now
                        </button>
                    </div>
                </div>
            </div>
        `;

        this.attachEvents();
    }

    attachEvents() {
        this.container.querySelectorAll('.academy-card, .btn-read-lesson').forEach(el => {
            el.addEventListener('click', (e) => {
                const topicId = el.getAttribute('data-topic-id');
                this.openTopic(topicId);
            });
        });

        const closeBtn = this.container.querySelector('#btn-close-academy');
        const modal = this.container.querySelector('#academy-modal');
        if (closeBtn && modal) {
            closeBtn.addEventListener('click', () => modal.classList.add('hidden'));
            modal.addEventListener('click', (e) => {
                if (e.target === modal) modal.classList.add('hidden');
            });
        }

        const practiceBtn = this.container.querySelector('#btn-modal-practice');
        if (practiceBtn) {
            practiceBtn.addEventListener('click', () => {
                if (this.selectedTopic && this.onPractice) {
                    if (modal) modal.classList.add('hidden');
                    this.onPractice(this.selectedTopic.practice_category, this.selectedTopic.practice_difficulty);
                }
            });
        }
    }

    openTopic(topicId) {
        const topic = this.topics.find(t => t.id === topicId);
        if (!topic) return;
        this.selectedTopic = topic;

        const modal = this.container.querySelector('#academy-modal');
        const catBadge = this.container.querySelector('#modal-category-badge');
        const titleEl = this.container.querySelector('#modal-topic-title');
        const bodyEl = this.container.querySelector('#modal-topic-body');

        catBadge.innerText = topic.category;
        titleEl.innerText = topic.title;

        let bodyHtml = `<p class="lesson-summary-lead">${topic.summary}</p><div class="lesson-sections">`;
        topic.sections.forEach(sec => {
            bodyHtml += `
                <div class="lesson-section-card">
                    <h4 class="section-title">${sec.title}</h4>
                    <p class="section-content">${sec.content}</p>
                </div>
            `;
        });
        bodyHtml += '</div>';

        bodyEl.innerHTML = bodyHtml;
        modal.classList.remove('hidden');
        if (window.soundEngine) window.soundEngine.playClick();
    }
}

window.AcademyController = AcademyController;
