import { siteConfig } from "@/data/site";
import type { Product } from "@/data/products";
import type { NewsItem } from "@/data/news";

const SITE_URL = "https://www.dubaicheng.com";

type LdNode = Record<string, unknown>;

/** 注入一段 JSON-LD,Server Component */
export function JsonLd({ data }: { data: LdNode }) {
  return (
    <script
      type="application/ld+json"
      // eslint-disable-next-line react/no-danger
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}

export function organizationLd(): LdNode {
  return {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: siteConfig.fullName,
    alternateName: siteConfig.name,
    url: SITE_URL,
    logo: `${SITE_URL}/icon.svg`,
    description: siteConfig.description,
    address: {
      "@type": "PostalAddress",
      streetAddress: siteConfig.contact.address,
      addressCountry: "CN",
    },
    contactPoint: {
      "@type": "ContactPoint",
      telephone: siteConfig.contact.phone,
      email: siteConfig.contact.email,
      contactType: "sales",
      availableLanguage: ["zh-CN", "en"],
    },
    sameAs: [SITE_URL],
  };
}

export function productLd(product: Product): LdNode {
  return {
    "@context": "https://schema.org",
    "@type": "Product",
    name: `${product.name} ${product.model}`,
    sku: product.model,
    category: product.category,
    description: product.description,
    brand: {
      "@type": "Brand",
      name: siteConfig.name,
    },
    manufacturer: {
      "@type": "Organization",
      name: siteConfig.fullName,
      url: SITE_URL,
    },
    additionalProperty: product.pillars.map((p) => ({
      "@type": "PropertyValue",
      name: p.label,
      value: p.value,
    })),
    url: `${SITE_URL}/products/${product.id}`,
  };
}

export function breadcrumbLd(
  items: { name: string; url: string }[],
): LdNode {
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: items.map((item, i) => ({
      "@type": "ListItem",
      position: i + 1,
      name: item.name,
      item: item.url.startsWith("http") ? item.url : `${SITE_URL}${item.url}`,
    })),
  };
}

export function articleLd(news: NewsItem): LdNode {
  return {
    "@context": "https://schema.org",
    "@type": "NewsArticle",
    headline: news.title,
    description: news.excerpt,
    datePublished: news.date,
    dateModified: news.date,
    author: {
      "@type": "Organization",
      name: siteConfig.fullName,
    },
    publisher: {
      "@type": "Organization",
      name: siteConfig.fullName,
      logo: {
        "@type": "ImageObject",
        url: `${SITE_URL}/icon.svg`,
      },
    },
    articleSection: news.category,
    url: `${SITE_URL}/news/${news.slug}`,
    mainEntityOfPage: {
      "@type": "WebPage",
      "@id": `${SITE_URL}/news/${news.slug}`,
    },
  };
}
