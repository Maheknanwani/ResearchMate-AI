def create_report(question, results, pages):

    report = f"""
# ResearchMate AI Research Report

## User Question

{question}

## Short Answer

The research agent collected information
from the following web sources.

## Key Findings
"""

    if pages:

        for page in pages:

            report += f"""

### {page['title']}

{page['text'][:700]}

Source: {page['url']}

"""

    else:

        report += """
No readable webpages were retrieved.
The research could not be completed reliably.
"""

    report += """
## Sources Used
"""

    for result in results:

        report += (
            f"- [{result['title']}]"
            f"({result['url']})\n"
        )

    report += """
## Confidence Level

Low to Medium. Confidence depends on source
quality and the completeness of retrieved information.

## Limitations

- Some websites may block automated access.
- Search results may be incomplete.
- Information should be independently verified.

## Suggested Next Steps

- Verify important findings.
- Compare information across multiple sources.
- Consult official documentation.
"""

    return report