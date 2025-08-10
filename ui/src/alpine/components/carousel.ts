class Carousel {
  currentIndex: number;
  items: HTMLElement[];

  constructor(items: HTMLElement[]) {
    this.items = items;
    this.currentIndex = 0;
    this.showCurrentItem();
  }

  showCurrentItem() {
    this.items.forEach((item, index) => {
      item.style.display = index === this.currentIndex ? 'block' : 'none';
    });
  }

  next() {
    this.currentIndex = (this.currentIndex + 1) % this.items.length;
    this.showCurrentItem();
  }

  previous() {
    this.currentIndex =
      (this.currentIndex - 1 + this.items.length) % this.items.length;
    this.showCurrentItem();
  }

  goTo(index: number) {
    if (index >= 0 && index < this.items.length) {
      this.currentIndex = index;
      this.showCurrentItem();
    }
  }
}

export default Carousel;
