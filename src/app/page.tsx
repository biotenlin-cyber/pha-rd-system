import { Hero } from "@/components/home/Hero";
import { Highlights } from "@/components/home/Highlights";
import { ProductPreview } from "@/components/home/ProductPreview";
import { AboutPreview } from "@/components/home/AboutPreview";
import { NewsPreview } from "@/components/home/NewsPreview";
import { CTASection } from "@/components/home/CTASection";

export default function HomePage() {
  return (
    <>
      <Hero />
      <Highlights />
      <ProductPreview />
      <AboutPreview />
      <NewsPreview />
      <CTASection />
    </>
  );
}
