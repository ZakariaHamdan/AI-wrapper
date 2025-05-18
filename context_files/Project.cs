using System.ComponentModel.DataAnnotations;

namespace RSG.Biovision.Domain.Entities;

public class Project : MainEntity
{
    [MaxLength(255)] public string? NameAr { get; set; }
    [Required] [MaxLength(255)] public string NameEn { get; set; }
    public string? ReferenceNo { get; set; }
    public DateTime StartDate { get; set; }
    public DateTime? EndDate { get; set; }
    public decimal? Budget { get; set; }
    public string? AddressAr { get; set; }
    public string? AddressEn { get; set; }

    public ICollection<MainContractorProject> MainContractorProjects { get; set; } = new List<MainContractorProject>();
    public virtual ICollection<Site> Sites { get; set; } = new List<Site>();


}
