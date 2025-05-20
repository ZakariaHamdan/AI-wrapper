using System.ComponentModel.DataAnnotations;
using RSG.Biovision.Domain.Entities.Interfaces;

namespace RSG.Biovision.Domain.Entities
{
    public class Notification : MainEntity, IHasCompany
    {
        [Required]
        public Guid UserId { get; set; }
        
        [Required]
        public Guid CompanyId { get; set; }
        
        [Required]
        [MaxLength(255)]
        public string Title { get; set; }
        
        [Required]
        public string Message { get; set; }
        
        [Required]
        public string? Type { get; set; }
        
        // Navigation properties
        public Company Company { get; set; }
    }
}